import traceback
import logging
import os
import subprocess
from logging import Logger

import matplotlib.pyplot as plt
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON, POST

from workflow_steps_utils import process_response_as_list, process_response_as_dict, now, to_human_datetime, ResponseType

# CONSTANTS
BASE_GRAPH = "http://smolang.org/dtdw"
QUERY_SERVER_URL = "http://localhost:3030/dtdw_deploy/sparql"
UPDATE_SERVER_URL = "http://localhost:3030/dtdw_deploy/update"
ALLOWED_TIME_DIFFERENCE_IN_SEC = 300  # 86400

#########################################

# Logger
logging.config.fileConfig("configs/logging.conf")

## Step class
class Step:

  def __init__(self, _sparql: SPARQLWrapper, _logger, _params: dict = None):
    """
    Initializes a Step object.

    Parameters:
        _sparql (SPARQL): SPARQLWrapper object.
        _params (dict): Dictionary with query parameters.
        _logger (Logger): Logger object
    """
    self.sparql = _sparql
    self.params = {} if _params is None else _params
    self.response = []
    self.logger = _logger

  def set_params(self, _params: dict):
    self.params = _params

  def query(self, _query: str) -> dict:
    """
    Execute query of the Step.

    Parameters:
        _query: SPARQL query
    Returns:
        dict: SPARQL query response as JSON/dict object.
    """
    self.logger.debug(f"query\n{_query}")

    self.sparql.setQuery(_query)
    _response = self.sparql.queryAndConvert()

    self.logger.debug(f"response\n{_response}")

    return _response


  def build_query(self) -> str:
    """
    Builds the SPARQL query to be executed for the step.

    Returns:
        str: SPARQL query string.
    """
    query = f"""
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?model_name WHERE {{ dtdw_deploy:{self.params['model']} dtdw_onto:{self.params['action']} ?model_name . }}
    """
    self.logger.debug(f"build_query\n{query}")
    return query

  def compare_time_diff(self, data: dict):
    time_diff = (abs(now() - int(
        data['executedAt'])) / 1000)  # timestamp is given in milliseconds
    if time_diff > ALLOWED_TIME_DIFFERENCE_IN_SEC:
      self.logger.error(
        f"Simulation result for '{data['availableIn']}' is older than {ALLOWED_TIME_DIFFERENCE_IN_SEC} seconds.")


  def get_compare_model_data_files(self, model_name: str) -> dict:
    """
    Extract list of data files from consumes model in the knowledge graph

    Parameters:
        model_name (str): Model name
    Returns:
        files (list): List of files
    """
    model_name = "compare_" + model_name
    query = f"""
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?consumes
      WHERE {{ dtdw_deploy:{model_name} dtdw_onto:consumes ?consumes . }}
    """
    self.logger.debug(f"extract list of data files query\n{query}")
    response = self.query(query)

    self.logger.debug(f"extracted list of data files results\n{response}")

    data_files = {}
    for _i, m in enumerate(
        process_response_as_list(response, ['consumes'], ResponseType.URI)):
      data_files[_i] = self.get_consumes_model_instance_data_file(m)

    return data_files


  def get_consumes_model_instance_data_file(self, consumes_model_instance: str) -> dict:
    """
    Extract consumes models data files name in the knowledge graph
    Parameters:
        consumes_model_instance (str): Consumes model instance
    Returns:
        filename (str): Filename
    """
    query = f"""
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?availableIn ?executedAt
      WHERE {{ dtdw_deploy:{consumes_model_instance} dtdw_onto:availableIn ?availableIn; dtdw_onto:executedAt ?executedAt . }}
      ORDER BY DESC(?executedAt)
      LIMIT 1
    """
    self.logger.debug(f"extract consumes \n{query}")

    return process_response_as_dict(self.query(query),['availableIn', 'executedAt'], ResponseType.LITERAL)


## LoadStep class
class LoadStep(Step):

  def __init__(self, _sparql: SPARQLWrapper = None, _logger=None,
      _params: dict = None):
    """
    Initializes a LoadStep object.

    Parameters:
        _sparql (SPARQL): SPARQLWrapper object.
        _logger (Logger): Logger object
        _params (dict): Dictionary with query parameters.
    """
    if _sparql is None:
      _sparql = SPARQLWrapper(QUERY_SERVER_URL)
      _sparql.setReturnFormat(JSON)

    if _logger is None:
      _logger = logging.getLogger("LoadStep")

    super().__init__(_sparql, _logger, _params)

  def get_produces_and_consumes(self, model, key):
    query = f"""
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?{key}
      WHERE {{dtdw_deploy:{model} dtdw_onto:{key} ?{key} . }}
    """
    return process_response_as_list(self.query(query), [key], ResponseType.URI)

  def get_available_in(self, model_instance: str,
      key: str = "availableIn") -> dict:
    """
    Builds the query and process the response from the server to obtain the model.

    Parameters:
        model_instance (str): Model instance name
        key (str): Response key
    Returns:
        list: Models for the step.
    """
    query = f"""
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?availableIn
      WHERE {{ dtdw_deploy:{model_instance} dtdw_onto:availableIn ?availableIn . }}
    """
    self.logger.debug(f"get_available_in query\n{query}")

    response = self.query(query)

    self.logger.debug(f"get_available_in response\n{response}")

    return {'key': model_instance, 'value':
      process_response_as_dict(response, [key], ResponseType.LITERAL)[key]}

  def get_models(self, _key: str) -> list:
    """
    Builds the query and process the response from the server to obtain the model.

    Parameters:
        _key (str): Response key to be extracted
    Returns:
        list: Models for the step.
    """
    _response = process_response_as_list(self.query(self.build_query()), [_key],
                                         ResponseType.URI)

    return [self.get_available_in(m) for m in _response]


## KnowledgeGraph class
class KnowledgeGraph(Step):

  def __init__(self, _sparql: SPARQLWrapper = None, _logger: Logger = None,
      _params: dict = None):
    """
    Initializes a KnowledgeGraph object.

    Parameters:
        _sparql (SPARQL): SPARQLWrapper object.
        _logger (Logger): Logger object
        _params (dict): Dictionary with query parameters.
    """
    self._step_name = None
    if _sparql is None:
      _sparql = SPARQLWrapper(QUERY_SERVER_URL)
      _sparql.setReturnFormat(JSON)

    if _logger is None:
      _logger = logging.getLogger("SimulateStep")

    super().__init__(_sparql, _logger, _params)
    self.step_models = {}
    self.simulation_parameters = {}

  def assert_model_file_exists(self, consumes_model_instance):
    load_step = LoadStep()
    filename = load_step.get_available_in(consumes_model_instance)['value'].strip()

    self.reset_path()

    # assert that file exist
    assert os.path.exists(filename.strip()), f"{filename} does not exist in directory."

  @staticmethod
  def reset_path():
    sub_directories = ['service_modelica', 'decoupled_model', 'cosim_modelica', 'monitor_service', 'logs']
    init_dir = os.getcwd()  # get initial directory
    # reset path to current file
    if init_dir in sub_directories:
      os.chdir('../')


  def run(self, _command: str, _dir: str = '', as_process: bool = False,
      split_char: str = ' ', delete_file_at_idx: int = 0) -> None:
    """
    Execute CMD commands
    """
    self.reset_path()
    init_dir = os.getcwd()  # get initial directory
    if _dir:
      os.chdir(_dir)  # change directory if dir variable is set

    if as_process:
      commands = _command.split(split_char)
      # remove csv file if it exists
      if delete_file_at_idx > 0 and os.path.exists(commands[delete_file_at_idx]):
        self.logger.info(f"deleting file: {commands[delete_file_at_idx]}")
        os.remove(commands[delete_file_at_idx])

      process_id = subprocess.Popen(commands)
      print(f"Run with process Id: {process_id.pid}")
      self.logger.info(f"Run with process Id: {process_id.pid}")

    else:
      cmd_output = subprocess.check_output(_command, shell=True, text=True)
      print(cmd_output)
      self.logger.info(f"{cmd_output}")

    if init_dir != os.getcwd():
      os.chdir(init_dir)  # if the initial and current directory is different, revert to the initial directory

  def last_executed_at(self, _model_type: str, _model_name: str) -> int:
    """
    Retrieve executedAt property value from Graph

    Parameters:
        _model_type (str): Model type
        _model_name (str): Model name
    Returns:
        int: Unix epoch timestamp
    """
    if _model_name == "":
      return 0

    _query = f"""
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      SELECT ?executedAt
      WHERE {{ ?model a dtdw_onto:DigitalTwinArtifact ; dtdw_onto:executedAt ?executedAt . FILTER (?model = dtdw_deploy:{_model_name} ) }}
      ORDER BY DESC(?executedAt)
      LIMIT 1
    """
    self.logger.debug(f"last_executed_at query\n{_query}")

    _dict = process_response_as_dict(self.query(_query), ['executedAt'], ResponseType.LITERAL)

    return _dict['executedAt'] if 'executedAt' in _dict else 0

  def build_query(self, model_name=None, action=None) -> str:
    """
    Builds the SPARQL query to be executed for the step.

    Returns:
        str: SPARQL query string.
    """
    if model_name is None:
      model_name = "simulate_" + self.params['model']  # Append prefix

    if action is None:
      action = self.params['action']

    _query = f"""
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?model_name
      WHERE {{ dtdw_deploy:{model_name} dtdw_onto:{action} ?model_name . }}
    """
    self.logger.debug(f"build_query\n{_query}")

    return _query

  def get_model(self, model_name=None, action=None, key: str = None) -> str:
    """
    Builds the query and process the response from the server to obtain the model.

    Returns:
          model: Model for the step.
    """
    if key is None:
      key = 'model_name'
    query = self.build_query(model_name, action)
    response = self.query(query)
    return process_response_as_dict(response, [key])[key]

  def initialize_step(self, _name: str):
    load_step = LoadStep()
    self._step_name =_name
    actions = []
    consumes = load_step.get_produces_and_consumes(self._step_name, 'consumes')
    if consumes:
      actions.append('consumes')

    produces = load_step.get_produces_and_consumes(self._step_name, 'produces')
    if produces:
      actions.append('produces')

    for action in actions:
      # LoadStep Parameters
      load_step.set_params({'model': self._step_name, 'action': action})

      # Load model
      response = load_step.get_models(_key='model_name')[0]

      # Add ontology key to model dictionary
      self.step_models[response['key']] = response['value']

      if 'consumes' == action:
        self.simulation_parameters['consumes_model_instance'] = response['key']

      if 'produces' == action:
        self.simulation_parameters['produces_model_instance'] = response['key']

    self.logger.info(f"The step contains the following model(s)/data: {self.step_models}")

    # Store step actions
    self.assert_model_file_exists(
        self.get_model(self._step_name, 'produces', 'model_name')
    )


  def run_simulation(self, simulation_params: dict) -> None:
    """
    Performs the simulation based of the models for the step.

    Parameters:
        simulation_params (dict): dictionary containing the models and data to be simulated.
    """
    self.simulation_parameters = {}
    for action in simulation_params['actions']:
      # Add action to query_params
      self.simulation_parameters['action'] = action
      simulation_params['action'] = action
      self.set_params(simulation_params)

      # Store step actions
      self.simulation_parameters[action] = self.get_model()

      # Add simulation file as step
      self.simulation_parameters['consumes_file'] = self.step_models[
        simulation_params['consumes']]

    produces, consumes = simulation_params['produces'], simulation_params[
      'consumes']

    self.simulation_parameters['path'] = simulation_params['path']
    self.simulation_parameters['method'] = simulation_params['method']
    self.simulation_parameters['cmd'] = simulation_params['cmd']

    __step = LoadStep(self.sparql, self.logger)
    filename = __step.get_available_in(consumes)['value'].strip()
    full_file_path = filename if not simulation_params['path'] else \
    simulation_params['path'] + '/' + filename
    new_execution_timestamp = now()

    # assert file exist
    assert os.path.exists(full_file_path.strip()), f"{full_file_path} does not exist in directory."

    # run consumes command to generate simulation results
    is_process = True if ('method' in simulation_params) and (
          simulation_params['method'].lower() == 'process') else False

    self.run(f"{simulation_params['cmd']} {filename}",
             simulation_params['path'], is_process)

    # compare current model lastExecutedAt timestamp against the lastExecutedAt from previous step
    self.compare_prior_step_timestamp(consumes, 'consumes')

    try:
      # update consumes
      if consumes:
        self.update_consumes_graph(new_execution_timestamp, consumes)

      # update produces
      if produces:
        self.update_produces_graph(new_execution_timestamp, produces)

      self.logger.info(f"Successfully executed simulation(s) for \'{consumes}\' at {to_human_datetime(new_execution_timestamp)}")

    except Exception as e:
      traceback.print_tb(e.__traceback__)
      self.logger.error(f"An error occurred while executing SPARQL update: {e}")

  def update_last_execution_timestamps(self):

    # Get current timestamp
    new_execution_timestamp = now()

    try:
      # Update consumes model lastExecutedAt timestamp
      if 'consumes_model_instance' in self.simulation_parameters:
        self.update_consumes_graph(new_execution_timestamp,
                                   self.simulation_parameters[
                                     'consumes_model_instance'])

      # Update produces model lastExecutedAt timestamp
      if 'produces_model_instance' in self.simulation_parameters:
        self.update_produces_graph(new_execution_timestamp,
                                   self.simulation_parameters[
                                     'produces_model_instance'])

      self.logger.info(f"Successfully updated execution timestamps the step at {to_human_datetime(new_execution_timestamp)}")

    except Exception as e:
      traceback.print_tb(e.__traceback__)
      self.logger.error(f"An error occurred while executing SPARQL update: {e}")

  def compare_prior_step_timestamp(self, _step_name: str = None, model_type: str = 'consumes'):
    """
    Compares the executedAt timestamp of the model being simulated against the previous model in the dependency graph

    Parameters:
        _step_name (str):
        model_type (str):
    """
    if _step_name is None and self._step_name:
      _step_name = self._step_name
    else:
      return
    step_order = self._get_step_order(_step_name)

    if step_order > 1:
      self.logger.info(f"Comparing model(s) last execution timestamp in step {_step_name} with model(s) in the previous step in the workflow!")

      previous_step = self._get_previous_step(step_order)

      # Get models in previous step
      previous_step_models = self._get_models_in_previous_step(previous_step)

      for _key in previous_step_models.keys():
        if _key in self.step_models:
          last_updated_at = int(previous_step_models[_key])

          time_diff = (abs(now() - last_updated_at) / 1000)  # timestamp is given in milliseconds

          if time_diff > ALLOWED_TIME_DIFFERENCE_IN_SEC:
            self.logger.error(f"Result(s) for model {_key} might be outdated, it was last executed at {to_human_datetime(last_updated_at)}")
    else:
      self.logger.info(f"{_step_name} is the first step of the workflow!")


  def _get_models_in_previous_step(self, _previous_step) -> dict:
    query = f"""
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT 
        ?model (MAX(xsd:integer(?executedAt)) AS ?last_updated_at)
      WHERE {{ dtdw_deploy:{_previous_step} dtdw_onto:consumes|dtdw_onto:produces  ?model . ?model dtdw_onto:executedAt ?executedAt . }}
      GROUP BY ?model
      ORDER BY DESC(?last_updated_at)
    """
    self.logger.debug(f"{query}")

    _response = self.query(query)

    data = {}
    processed_models = process_response_as_list(_response, ['model'], ResponseType.URI)
    if processed_models:
      timestamps = process_response_as_list(_response, ['last_updated_at'], ResponseType.LITERAL)
      for i, z in enumerate(processed_models):
        data[z] = timestamps[i]

    return data

  def _get_step_order(self, _step_name) -> int:
    query = f"""
      prefix xsd: <http://www.w3.org/2001/XMLSchema#>
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?order
      WHERE {{ VALUES ?inst {{ dtdw_deploy:{_step_name} }} ?inst dtdw_onto:order ?order . }}
    """
    self.logger.debug(f"{query}")

    _dict = process_response_as_dict(self.query(query),['order'], ResponseType.LITERAL)

    return int(_dict['order']) if 'order' in _dict else -1

  def _get_previous_step(self, _current_step_idx:int, _process:str="MixConcreteProcess") -> str:
    if _current_step_idx < 2:
      self.logger.error("Index of current step must be greater of equal to 1.")
      return ""

    query = f"""
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
      PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
      PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
      SELECT ?step ?order
      WHERE {{ dtdw_deploy:{_process} ( dtdw_onto:hasStep ) ?step . ?step dtdw_onto:order ?order .  FILTER (?order={_current_step_idx - 1}) }}
    """
    self.logger.debug(f"{query}")

    response = self.query(query)

    # process response
    _steps_dict = process_response_as_dict(response, ['step'], ResponseType.URI)

    return _steps_dict['step'] if _steps_dict and 'step' in _steps_dict else ""

  def update_consumes_graph(self, new_timestamp: int, _model: str) -> None:
    return self._update_graph(new_timestamp, _model, 'consumes')


  def update_produces_graph(self, new_timestamp: int, _model: str) -> None:
    return self._update_graph(new_timestamp, _model, 'produces')


  def _update_graph(self, new_timestamp: int, _model: str,
      model_type: str) -> None:
    """
    Stores simulation results into the knowledge graph

    Parameters:
        new_timestamp (int):
        _model (str): dictionary containing the query parameter data.
        model_type (str): dictionary containing the query parameter data.
    """
    _sparql = SPARQLWrapper(UPDATE_SERVER_URL)
    _sparql.setReturnFormat(JSON)
    _params = {
      'graph': f"{BASE_GRAPH}/dtdw_deploy",
      'old_timestamp': self.last_executed_at(model_type, _model),
      'new_timestamp': new_timestamp
    }

    try:
      query = f"""
          PREFIX dtdw_deploy: <{BASE_GRAPH}/dtdw_deploy#>
          PREFIX dtdw_onto: <{BASE_GRAPH}/dtdw_onto#>
          INSERT {{ GRAPH <{_params['graph']}> {{ dtdw_deploy:{_model} dtdw_onto:executedAt {_params['new_timestamp']} }} }}
          USING <{_params['graph']}>
          WHERE {{ dtdw_deploy:{_model} dtdw_onto:executedAt {_params['old_timestamp']} }}
      """
      _sparql.setQuery(query)
      _sparql.setMethod(POST)  # Use POST for update queries
      _sparql.query().convert()

    except Exception as e:
      traceback.print_tb(e.__traceback__)
      self.logger.error(f"An error occurred updating graph: {e}")


  def validate_model_last_execution_timestamps(self):
    if self._step_name is None:
      return

    model_files = self.get_compare_model_data_files(self._step_name)
    for i in model_files:
      self.compare_time_diff(model_files[i])


## CompareStep class
class CompareStep(Step):

  def __init__(self, _sparql: SPARQLWrapper = None, _logger: Logger = None,
      _params=None):
    """
    Initializes a CompareStep object.

    Parameters:
        _sparql (SPARQL): SPARQLWrapper object.
        _params : Dictionary with query parameters.
    """
    if _sparql is None:
      _sparql = SPARQLWrapper(QUERY_SERVER_URL)
      _sparql.setReturnFormat(JSON)

    if _logger is None:
      _logger = logging.getLogger("CompareStep")

    super().__init__(_sparql, _logger, _params)

  def plot_graph(self, _simulation_data: dict, x_label: str = 'Time',
      y_label: str = 'Angle (rad)', start_from: int = None) -> None:
    """
    Plot simulation results

    Parameters:
        _simulation_data (dict): Plot data information
        x_label (str): x-axis label
        y_label (str): y-axis label
        start_from(int): Starting dataframe index
    """
    assert _simulation_data['model'], "Simulation data dictionary requires 'model' key"

    try:
      _simulation_data['files'] = self.get_compare_model_data_files(_simulation_data['model'])

      for i in _simulation_data['files']:
        self.compare_time_diff(_simulation_data['files'][i])

      assert len(_simulation_data['files']) == len(
          _simulation_data['plot_data']), "plot data files size do not match"

      for i in _simulation_data['plot_data']:
        full_file_path = _simulation_data['files'][i]['availableIn'].strip()

        assert os.path.exists(
          full_file_path), f"{full_file_path} does not exist in directory."

        df = pd.read_csv(full_file_path)
        if start_from is not None:
          df = df.iloc[start_from:, :]

        for _d in _simulation_data['plot_data'][i]:
          plt.plot(df[_d['x']], df[_d['y']], label=_d['label'],
                   color=_d['color'],
                   linestyle=_d['line'] if _d['line'] else '-')

      plt.xlabel(x_label)
      plt.ylabel(y_label)
      plt.legend()
      plt.show()
    except Exception as e:
      traceback.print_tb(e.__traceback__)
      self.logger.error(f"An error occurred during plotting of data. \nException: {e}.")
