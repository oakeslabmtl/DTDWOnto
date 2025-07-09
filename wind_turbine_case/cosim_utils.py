import subprocess
import pandas as pd
import json

def run_experiment_with_step_size(step_size, scenario_template, scenario_output, dir_ = "cosim_modelica"):
  coe_command = f"java -jar maestro.jar import Sg1 -output=results -v --interpret --fmu-search-path FMUs {scenario_output}"

  # Set the step size in the config file:
  search_and_replace("0.001", str(step_size), scenario_template, scenario_output, dir_)

  result = subprocess.run(coe_command, shell=True, capture_output=True, text=True, cwd=dir_)

  # Check for failure and print debug information
  if result.returncode != 0:
    with open(scenario_output, 'r') as file:
        scenario_raw = file.read()
    raise RuntimeError(f"Error running command {coe_command} for step size {step_size}: {result.stderr}. \nThe input scenario is:\n{json.dumps(json.loads(scenario_raw), indent=2)}")

  # Read results and compute error
  data = pd.read_csv(dir_ + "/" + "results/outputs.csv" if dir_ != "" else "results/outputs.csv")
  return data

# So we need a function to run a full experiment given a step size.
def search_and_replace(key, value, file_src, file_trg, dir_):
  '''
  Opens a file fileSrc and searches for all occurrences of key string and replaces it by value.
  Stores the result in fileTrg.
  '''
  file_src = dir_ + "/" + file_src if dir_ != "" else file_src
  file_trg = dir_ + "/" + file_trg if dir_ != "" else file_trg

  with open(file_src, 'r') as file :
    file_data = file.read()

  file_data = file_data.replace(key, value)

  with open(file_trg, 'w') as file:
    file.write(file_data)
