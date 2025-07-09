from fmpy.fmi2 import FMU2Slave

# Support functions for loading FMUs
def build_logging_function(logger):
    def logging_function(msg):
        logger.debug(msg)
    return logging_function

def getVars(model_description):
    vrs = {}
    for variable in model_description.modelVariables:
        vrs[variable.name] = variable
    return vrs

def load(fmu_path, model_description, instanceName, logging_function):
    # Check if its a zip file and if so, extract
    if fmu_path.endswith('.zip'):
        unzipdir = extract(fmu_path)
    else:
        unzipdir = fmu_path
    
    fmu = FMU2Slave(guid=model_description.guid,
                    unzipDirectory=unzipdir,
                    modelIdentifier=model_description.coSimulation.modelIdentifier,
                    instanceName=instanceName, 
                    fmiCallLogger=logging_function)
    return fmu, unzipdir
