/* Main Simulation File */

#if defined(__cplusplus)
extern "C" {
#endif

#include "DutMonitor_model.h"
#include "simulation/solver/events.h"



/* dummy VARINFO and FILEINFO */
const FILE_INFO dummyFILE_INFO = omc_dummyFileInfo;
const VAR_INFO dummyVAR_INFO = omc_dummyVarInfo;

int DutMonitor_input_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  (data->localData[0]->realVars[4]/* dut_out_acceleration variable */)  = data->simulationInfo->inputVars[0];
  (data->localData[0]->realVars[5]/* dut_out_angle variable */)  = data->simulationInfo->inputVars[1];
  (data->localData[0]->realVars[6]/* dut_out_speed variable */)  = data->simulationInfo->inputVars[2];
  (data->localData[0]->realVars[7]/* dut_out_torque variable */)  = data->simulationInfo->inputVars[3];
  (data->localData[0]->realVars[11]/* in_acceleration variable */)  = data->simulationInfo->inputVars[4];
  (data->localData[0]->realVars[12]/* in_angle variable */)  = data->simulationInfo->inputVars[5];
  (data->localData[0]->realVars[13]/* in_set_torque variable */)  = data->simulationInfo->inputVars[6];
  (data->localData[0]->realVars[14]/* in_speed variable */)  = data->simulationInfo->inputVars[7];
  
  TRACE_POP
  return 0;
}

int DutMonitor_input_function_init(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->inputVars[0] = data->modelData->realVarsData[4].attribute.start;
  data->simulationInfo->inputVars[1] = data->modelData->realVarsData[5].attribute.start;
  data->simulationInfo->inputVars[2] = data->modelData->realVarsData[6].attribute.start;
  data->simulationInfo->inputVars[3] = data->modelData->realVarsData[7].attribute.start;
  data->simulationInfo->inputVars[4] = data->modelData->realVarsData[11].attribute.start;
  data->simulationInfo->inputVars[5] = data->modelData->realVarsData[12].attribute.start;
  data->simulationInfo->inputVars[6] = data->modelData->realVarsData[13].attribute.start;
  data->simulationInfo->inputVars[7] = data->modelData->realVarsData[14].attribute.start;
  
  TRACE_POP
  return 0;
}

int DutMonitor_input_function_updateStartValues(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->modelData->realVarsData[4].attribute.start = data->simulationInfo->inputVars[0];
  data->modelData->realVarsData[5].attribute.start = data->simulationInfo->inputVars[1];
  data->modelData->realVarsData[6].attribute.start = data->simulationInfo->inputVars[2];
  data->modelData->realVarsData[7].attribute.start = data->simulationInfo->inputVars[3];
  data->modelData->realVarsData[11].attribute.start = data->simulationInfo->inputVars[4];
  data->modelData->realVarsData[12].attribute.start = data->simulationInfo->inputVars[5];
  data->modelData->realVarsData[13].attribute.start = data->simulationInfo->inputVars[6];
  data->modelData->realVarsData[14].attribute.start = data->simulationInfo->inputVars[7];
  
  TRACE_POP
  return 0;
}

int DutMonitor_inputNames(DATA *data, char ** names){
  TRACE_PUSH

  names[0] = (char *) data->modelData->realVarsData[4].info.name;
  names[1] = (char *) data->modelData->realVarsData[5].info.name;
  names[2] = (char *) data->modelData->realVarsData[6].info.name;
  names[3] = (char *) data->modelData->realVarsData[7].info.name;
  names[4] = (char *) data->modelData->realVarsData[11].info.name;
  names[5] = (char *) data->modelData->realVarsData[12].info.name;
  names[6] = (char *) data->modelData->realVarsData[13].info.name;
  names[7] = (char *) data->modelData->realVarsData[14].info.name;
  
  TRACE_POP
  return 0;
}

int DutMonitor_data_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  TRACE_POP
  return 0;
}

int DutMonitor_dataReconciliationInputNames(DATA *data, char ** names){
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int DutMonitor_output_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->outputVars[0] = (data->localData[0]->realVars[15]/* out_conformance variable */) ;
  
  TRACE_POP
  return 0;
}

int DutMonitor_setc_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


/*
equation index: 9
type: SIMPLE_ASSIGN
$DER.dut_turbine.phi = in_speed
*/
void DutMonitor_eqFunction_9(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,9};
  (data->localData[0]->realVars[0]/* der(dut_turbine.phi) DUMMY_DER */)  = (data->localData[0]->realVars[14]/* in_speed variable */) ;
  TRACE_POP
}
/*
equation index: 10
type: SIMPLE_ASSIGN
dut_turbine.w = in_speed
*/
void DutMonitor_eqFunction_10(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,10};
  (data->localData[0]->realVars[10]/* dut_turbine.w DUMMY_STATE */)  = (data->localData[0]->realVars[14]/* in_speed variable */) ;
  TRACE_POP
}
/*
equation index: 11
type: SIMPLE_ASSIGN
dut_turbine.phi = in_angle
*/
void DutMonitor_eqFunction_11(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,11};
  (data->localData[0]->realVars[9]/* dut_turbine.phi DUMMY_STATE */)  = (data->localData[0]->realVars[12]/* in_angle variable */) ;
  TRACE_POP
}
/*
equation index: 12
type: SIMPLE_ASSIGN
out_conformance = add.k1 * in_speed + add.k2 * dut_out_speed
*/
void DutMonitor_eqFunction_12(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,12};
  (data->localData[0]->realVars[15]/* out_conformance variable */)  = ((data->simulationInfo->realParameter[0]/* add.k1 PARAM */) ) * ((data->localData[0]->realVars[14]/* in_speed variable */) ) + ((data->simulationInfo->realParameter[1]/* add.k2 PARAM */) ) * ((data->localData[0]->realVars[6]/* dut_out_speed variable */) );
  TRACE_POP
}
/*
equation index: 13
type: SIMPLE_ASSIGN
dut_turbine.a = DutMonitor.angleToTorqueAdaptor.move.position_der2({in_angle, in_speed, in_acceleration}, time, 1.0, 0.0)
*/
void DutMonitor_eqFunction_13(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,13};
  real_array tmp0;
  array_alloc_scalar_real_array(&tmp0, 3, (modelica_real)(data->localData[0]->realVars[12]/* in_angle variable */) , (modelica_real)(data->localData[0]->realVars[14]/* in_speed variable */) , (modelica_real)(data->localData[0]->realVars[11]/* in_acceleration variable */) );
  (data->localData[0]->realVars[8]/* dut_turbine.a variable */)  = omc_DutMonitor_angleToTorqueAdaptor_move_position__der2(threadData, tmp0, data->localData[0]->timeValue, 1.0, 0.0);
  TRACE_POP
}
/*
equation index: 14
type: SIMPLE_ASSIGN
angleToTorqueAdaptor.tau = in_set_torque + dut_turbine.J * dut_turbine.a
*/
void DutMonitor_eqFunction_14(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,14};
  (data->localData[0]->realVars[3]/* angleToTorqueAdaptor.tau variable */)  = (data->localData[0]->realVars[13]/* in_set_torque variable */)  + ((data->simulationInfo->realParameter[2]/* dut_turbine.J PARAM */) ) * ((data->localData[0]->realVars[8]/* dut_turbine.a variable */) );
  TRACE_POP
}
/*
equation index: 15
type: SIMPLE_ASSIGN
$DER.dut_turbine.w = dut_turbine.a
*/
void DutMonitor_eqFunction_15(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,15};
  (data->localData[0]->realVars[1]/* der(dut_turbine.w) DUMMY_DER */)  = (data->localData[0]->realVars[8]/* dut_turbine.a variable */) ;
  TRACE_POP
}

OMC_DISABLE_OPT
int DutMonitor_functionDAE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  int equationIndexes[1] = {0};
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_DAE);
#endif

  data->simulationInfo->needToIterate = 0;
  data->simulationInfo->discreteCall = 1;
  DutMonitor_functionLocalKnownVars(data, threadData);
  DutMonitor_eqFunction_9(data, threadData);

  DutMonitor_eqFunction_10(data, threadData);

  DutMonitor_eqFunction_11(data, threadData);

  DutMonitor_eqFunction_12(data, threadData);

  DutMonitor_eqFunction_13(data, threadData);

  DutMonitor_eqFunction_14(data, threadData);

  DutMonitor_eqFunction_15(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_DAE);
#endif
  TRACE_POP
  return 0;
}


int DutMonitor_functionLocalKnownVars(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


int DutMonitor_functionODE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_FUNCTION_ODE);
#endif

  
  data->simulationInfo->callStatistics.functionODE++;
  
  DutMonitor_functionLocalKnownVars(data, threadData);
  /* no ODE systems */

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_FUNCTION_ODE);
#endif

  TRACE_POP
  return 0;
}

/* forward the main in the simulation runtime */
extern int _main_SimulationRuntime(int argc, char**argv, DATA *data, threadData_t *threadData);

#include "DutMonitor_12jac.h"
#include "DutMonitor_13opt.h"

struct OpenModelicaGeneratedFunctionCallbacks DutMonitor_callback = {
   NULL,    /* performSimulation */
   NULL,    /* performQSSSimulation */
   NULL,    /* updateContinuousSystem */
   DutMonitor_callExternalObjectDestructors,    /* callExternalObjectDestructors */
   NULL,    /* initialNonLinearSystem */
   NULL,    /* initialLinearSystem */
   NULL,    /* initialMixedSystem */
   #if !defined(OMC_NO_STATESELECTION)
   DutMonitor_initializeStateSets,
   #else
   NULL,
   #endif    /* initializeStateSets */
   DutMonitor_initializeDAEmodeData,
   DutMonitor_functionODE,
   DutMonitor_functionAlgebraics,
   DutMonitor_functionDAE,
   DutMonitor_functionLocalKnownVars,
   DutMonitor_input_function,
   DutMonitor_input_function_init,
   DutMonitor_input_function_updateStartValues,
   DutMonitor_data_function,
   DutMonitor_output_function,
   DutMonitor_setc_function,
   DutMonitor_function_storeDelayed,
   DutMonitor_function_storeSpatialDistribution,
   DutMonitor_function_initSpatialDistribution,
   DutMonitor_updateBoundVariableAttributes,
   DutMonitor_functionInitialEquations,
   1, /* useHomotopy - 0: local homotopy (equidistant lambda), 1: global homotopy (equidistant lambda), 2: new global homotopy approach (adaptive lambda), 3: new local homotopy approach (adaptive lambda)*/
   NULL,
   DutMonitor_functionRemovedInitialEquations,
   DutMonitor_updateBoundParameters,
   DutMonitor_checkForAsserts,
   DutMonitor_function_ZeroCrossingsEquations,
   DutMonitor_function_ZeroCrossings,
   DutMonitor_function_updateRelations,
   DutMonitor_zeroCrossingDescription,
   DutMonitor_relationDescription,
   DutMonitor_function_initSample,
   DutMonitor_INDEX_JAC_A,
   DutMonitor_INDEX_JAC_B,
   DutMonitor_INDEX_JAC_C,
   DutMonitor_INDEX_JAC_D,
   DutMonitor_INDEX_JAC_F,
   DutMonitor_initialAnalyticJacobianA,
   DutMonitor_initialAnalyticJacobianB,
   DutMonitor_initialAnalyticJacobianC,
   DutMonitor_initialAnalyticJacobianD,
   DutMonitor_initialAnalyticJacobianF,
   DutMonitor_functionJacA_column,
   DutMonitor_functionJacB_column,
   DutMonitor_functionJacC_column,
   DutMonitor_functionJacD_column,
   DutMonitor_functionJacF_column,
   DutMonitor_linear_model_frame,
   DutMonitor_linear_model_datarecovery_frame,
   DutMonitor_mayer,
   DutMonitor_lagrange,
   DutMonitor_pickUpBoundsForInputsInOptimization,
   DutMonitor_setInputData,
   DutMonitor_getTimeGrid,
   DutMonitor_symbolicInlineSystem,
   DutMonitor_function_initSynchronous,
   DutMonitor_function_updateSynchronous,
   DutMonitor_function_equationsSynchronous,
   DutMonitor_inputNames,
   DutMonitor_dataReconciliationInputNames,
   DutMonitor_read_input_fmu,
   NULL,
   NULL,
   -1,
   NULL,
   NULL,
   -1

};

#define _OMC_LIT_RESOURCE_0_name_data "Complex"
#define _OMC_LIT_RESOURCE_0_dir_data "C:/Users/D48113/AppData/Roaming/.openmodelica/libraries/Complex 4.0.0+maint.om"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_name,7,_OMC_LIT_RESOURCE_0_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir,78,_OMC_LIT_RESOURCE_0_dir_data);

#define _OMC_LIT_RESOURCE_1_name_data "DutMonitor"
#define _OMC_LIT_RESOURCE_1_dir_data "C:/work/github/2023.IncubatorOnto/code/example_methodology/service_modelica"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_name,10,_OMC_LIT_RESOURCE_1_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir,75,_OMC_LIT_RESOURCE_1_dir_data);

#define _OMC_LIT_RESOURCE_2_name_data "Modelica"
#define _OMC_LIT_RESOURCE_2_dir_data "C:/Users/D48113/AppData/Roaming/.openmodelica/libraries/Modelica 4.0.0+maint.om"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_name,8,_OMC_LIT_RESOURCE_2_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir,79,_OMC_LIT_RESOURCE_2_dir_data);

#define _OMC_LIT_RESOURCE_3_name_data "ModelicaServices"
#define _OMC_LIT_RESOURCE_3_dir_data "C:/Users/D48113/AppData/Roaming/.openmodelica/libraries/ModelicaServices 4.0.0+maint.om"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_name,16,_OMC_LIT_RESOURCE_3_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir,87,_OMC_LIT_RESOURCE_3_dir_data);

static const MMC_DEFSTRUCTLIT(_OMC_LIT_RESOURCES,8,MMC_ARRAY_TAG) {MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir)}};
void DutMonitor_setupDataStruc(DATA *data, threadData_t *threadData)
{
  assertStreamPrint(threadData,0!=data, "Error while initialize Data");
  threadData->localRoots[LOCAL_ROOT_SIMULATION_DATA] = data;
  data->callback = &DutMonitor_callback;
  OpenModelica_updateUriMapping(threadData, MMC_REFSTRUCTLIT(_OMC_LIT_RESOURCES));
  data->modelData->modelName = "DutMonitor";
  data->modelData->modelFilePrefix = "DutMonitor";
  data->modelData->resultFileName = NULL;
  data->modelData->modelDir = "C:/work/github/2023.IncubatorOnto/code/example_methodology/service_modelica";
  data->modelData->modelGUID = "{9b7de503-a73e-4434-8bfa-2ae316e320c7}";
  data->modelData->initXMLData = NULL;
  data->modelData->modelDataXml.infoXMLData = NULL;
  data->modelData->runTestsuite = 0;
  
  data->modelData->nStates = 0;
  data->modelData->nVariablesReal = 16;
  data->modelData->nDiscreteReal = 0;
  data->modelData->nVariablesInteger = 0;
  data->modelData->nVariablesBoolean = 0;
  data->modelData->nVariablesString = 0;
  data->modelData->nParametersReal = 3;
  data->modelData->nParametersInteger = 4;
  data->modelData->nParametersBoolean = 5;
  data->modelData->nParametersString = 0;
  data->modelData->nInputVars = 8;
  data->modelData->nOutputVars = 1;
  
  data->modelData->nAliasReal = 38;
  data->modelData->nAliasInteger = 0;
  data->modelData->nAliasBoolean = 0;
  data->modelData->nAliasString = 0;
  
  data->modelData->nZeroCrossings = 0;
  data->modelData->nSamples = 0;
  data->modelData->nRelations = 0;
  data->modelData->nMathEvents = 0;
  data->modelData->nExtObjs = 0;
  
  GC_asprintf(&data->modelData->modelDataXml.fileName, "%s/DutMonitor_info.json", data->modelData->resourcesDir);
  data->modelData->modelDataXml.modelInfoXmlLength = 0;
  data->modelData->modelDataXml.nFunctions = 1;
  data->modelData->modelDataXml.nProfileBlocks = 0;
  data->modelData->modelDataXml.nEquations = 28;
  data->modelData->nMixedSystems = 0;
  data->modelData->nLinearSystems = 0;
  data->modelData->nNonLinearSystems = 0;
  data->modelData->nStateSets = 0;
  data->modelData->nJacobians = 5;
  data->modelData->nOptimizeConstraints = 0;
  data->modelData->nOptimizeFinalConstraints = 0;
  
  data->modelData->nDelayExpressions = 0;
  
  data->modelData->nBaseClocks = 0;
  
  data->modelData->nSpatialDistributions = 0;
  
  data->modelData->nSensitivityVars = 0;
  data->modelData->nSensitivityParamVars = 0;
  data->modelData->nSetcVars = 0;
  data->modelData->ndataReconVars = 0;
  data->modelData->linearizationDumpLanguage =
  OMC_LINEARIZE_DUMP_LANGUAGE_MODELICA;
}

static int rml_execution_failed()
{
  fflush(NULL);
  fprintf(stderr, "Execution failed!\n");
  fflush(NULL);
  return 1;
}

