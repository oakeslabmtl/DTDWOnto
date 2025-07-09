from __future__ import annotations

import os
import glob
import docker
import subprocess
import time
import logging
import requests
from logging import Logger
from requests.exceptions import ConnectionError
from docker.errors import NotFound, APIError
from datetime import datetime as dt, datetime
from enum import Enum
from pyhocon import ConfigFactory

OMC_EXTENSIONS = ["o", "c", "h", "libs", "log", "bat", "makefile", "exe", "json", "xml"]
DEFAULT_DOCKER_COMPOSE_COMMAND = "docker compose up --detach --build"

class ResponseType(Enum):
  URI = 1
  LITERAL = 2


## Helper functions
def seconds_to_hours(seconds: int) -> str:
  return str(seconds//3600) + " hour(s)"


def delete_file_with_extension(extension: str, dir_: str = '.') -> None:
  """
  Delete files by extension

  Parameters:
      extension (str): Extension to be deleted
      dir_(str): The directory of the files
  """
  _logger = logging.getLogger("DeleteFileWithExtension")
  # get a list of files with the specified extension
  files_to_delete = glob.glob(f"*.{extension}", root_dir=dir_)

  # delete each file
  for file_path in files_to_delete:
    try:
      os.remove(os.path.join(dir_, file_path))
    except Exception as e:
      _logger.error(f"Error deleting {file_path}: {e}")


def delete_files_with_extension(extensions=None, _dir: str = '.') -> None:
  """
  Delete files by extensions

  Parameters:
      extensions (str): List of the extensions to be deleted
      _dir(str): The directory of the files
  """
  if extensions is None:
    extensions = OMC_EXTENSIONS

  for extension in extensions:
    delete_file_with_extension(extension, _dir)


def now() -> int:
  """
  Retrieve current timestamp as UNIX epoch value

  Returns:
      int: UNIX timestamp
  """
  return int(dt.timestamp(dt.now()) * 1000)


def to_human_datetime(unix_epoch_timestamp:int) -> str | datetime:
  """
  Convert Unix integer datetime to human-readable datetime format

  Parameters:
      unix_epoch_timestamp (int): Unix integer datetime

  Returns:
      human_datetime (str): human-readable datetime
  """
  if unix_epoch_timestamp == 0:
    return '0'
  return  dt.fromtimestamp(unix_epoch_timestamp / 1000)


def process_response_as_dict(res: dict, keys: list, res_type: ResponseType = ResponseType.URI):
  """
  Process response's JSON object

  Parameters:
      res (dict): Response object
      keys (list): list of keys to be extracted
      res_type: URI | LITERAL

  Returns:
      dict: SPARQL query response as JSON/dict object.
  """
  _data = {}
  if 'results' in res.keys() and res['results']:
    for binding in res['results']['bindings']:
      _value = {}
      for k in keys:
        _value[k] = str(binding[k]['value'])
        _data[k] = _value[k].split('#')[1] if res_type == ResponseType.URI else _value[k]
  return _data


def process_response_as_list(res: dict, keys: list, res_type: ResponseType = ResponseType.URI):
  """
  Process response's JSON object

  Parameters:
      res (dict): Response object
      keys (list): list of keys to be extracted
      res_type: URI | LITERAL

  Returns:
      list: SPARQL query response as JSON/dict object.
  """
  _data = []
  if 'results' in res.keys() and res['results']:
    for binding in res['results']['bindings']:
      _value = {}
      for k in keys:
        _value[k] = str(binding[k]['value'])
        _data.append(_value[k].split('#')[1] if res_type == ResponseType.URI else _value[k])
  return _data

def load_config(config_file_name) -> dict:
  file_path = resource_file_path(config_file_name)
  config = ConfigFactory.parse_file(file_path)
  return config

def resource_file_path(f):
  python_path = os.environ.get("PYTHONPATH")
  if python_path is None:
    directories = ['.']
  else:
    directories = python_path.split(os.pathsep) + ['.']

  for d in directories:
    filepath = os.path.join(d, f)
    if os.path.exists(filepath):
      return filepath

  print(f"File not found: {f}")
  print("Tried the following directories:")
  print(directories)

  raise ValueError(f"File not found: {f}")


class DockerContainerService:

  def __init__(self, container_name: str, logger: logging.Logger):
    self._container_name = container_name
    self._logger = logger


  def kill_container(self):
    self._logger.info("Searching for container with the name: " + self._container_name)
    client = docker.from_env()
    try:
      container = client.containers.get(self._container_name)
      self._logger.info(f"Container status: {container.status}")

      if container.status == "running":
        self._logger.info("Container is running. Issuing kill request.")
        container.kill()

        self._logger.info(client.containers.get(self._container_name).status)
      assert client.containers.get(self._container_name).status != "running"

    except (NotFound, APIError) as x:
      self._logger.error(f"Exception in attempt to kill container: {str(x)}")

    finally:
      client.close()


  def start_container(self, log_file_path, docker_compose_directory_path, test_connection_function=None, sleep_time:int=1, max_attempts:int=10):
    self._logger.info(f"Log will be stored in: {os.path.abspath(log_file_path)}")

    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    with open(log_file_path, "wt") as f:
      self._logger.info(f"Running docker-compose command: {DEFAULT_DOCKER_COMPOSE_COMMAND}")

      proc = subprocess.run(DEFAULT_DOCKER_COMPOSE_COMMAND, cwd=docker_compose_directory_path, shell=True, stdout=f)
      if proc.returncode == 0:
        self._logger.info("docker-compose successful.")
      else:
        self._logger.info(f"docker-composed failed: {str(proc.returncode)}")
        return False
      service_ready = False
      attempts = max_attempts

      while service_ready is False and attempts > 0:
        if test_connection_function is not None:
          r = test_connection_function()
          if r is True:
            self._logger.info("Service is ready")
            service_ready = True
          else:
            attempts -= 1
            self._logger.info("Service is not ready yet. Attempts remaining:" + str(attempts))
            if attempts > 0:
              time.sleep(sleep_time)
        else:
          self._logger.debug("Empty test_connection_function provided")
          self._logger.info("Service is ready")
          service_ready = True


class RabbitMQDockerService(DockerContainerService):

  def __init__(self, logger: Logger, container_name:str = "rabbitmq", log_file_name = "logs/rabbitmq.log"):
    super().__init__(container_name, logger)
    self._log_file_name = log_file_name
    self._docker_compose_directory_path = resource_file_path("rabbitmq_server")
    self.configs = load_config("rabbitmq_server/rabbitmq.conf")
    self._default_user = self.configs["default_user"] if self.configs else ""
    self._default_pass = self.configs["default_pass"] if self.configs else ""


  def _test_connection_function(self):
    try:
      r = requests.get("http://localhost:15672/api/overview", auth=(self._default_user, self._default_pass))
      if r.status_code == 200:
        self._logger.info(f"{self._container_name} ready:\n {r.text}")
        print(f"{self._container_name} ready")
        return True

    except ConnectionError as e:
      self._logger.error(f"{self._container_name} not ready - Exception: {e.__class__.__name__}")
    return False


  def start(self):
    self.kill_container()
    self.start_container(self._log_file_name, self._docker_compose_directory_path, self._test_connection_function, 1, 10)

  def stop(self):
    self.kill_container()