/* Initialization */
#include "DutMonitor_model.h"
#include "DutMonitor_11mix.h"
#include "DutMonitor_12jac.h"
#if defined(__cplusplus)
extern "C" {
#endif

void DutMonitor_functionInitialEquations_0(DATA *data, threadData_t *threadData);

/*
equation index: 1
type: SIMPLE_ASSIGN
angleToTorqueAdaptor.move.phi_support = 0.0
*/
void DutMonitor_eqFunction_1(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,1};
  (data->localData[0]->realVars[2]/* angleToTorqueAdaptor.move.phi_support variable */)  = 0.0;
  TRACE_POP
}
extern void DutMonitor_eqFunction_10(DATA *data, threadData_t *threadData);


/*
equation index: 3
type: SIMPLE_ASSIGN
out_conformance = add.k1 * dut_turbine.w + add.k2 * dut_out_speed
*/
void DutMonitor_eqFunction_3(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,3};
  (data->localData[0]->realVars[15]/* out_conformance variable */)  = ((data->simulationInfo->realParameter[0]/* add.k1 PARAM */) ) * ((data->localData[0]->realVars[10]/* dut_turbine.w DUMMY_STATE */) ) + ((data->simulationInfo->realParameter[1]/* add.k2 PARAM */) ) * ((data->localData[0]->realVars[6]/* dut_out_speed variable */) );
  TRACE_POP
}

/*
equation index: 4
type: SIMPLE_ASSIGN
$DER.dut_turbine.phi = dut_turbine.w
*/
void DutMonitor_eqFunction_4(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,4};
  (data->localData[0]->realVars[0]/* der(dut_turbine.phi) DUMMY_DER */)  = (data->localData[0]->realVars[10]/* dut_turbine.w DUMMY_STATE */) ;
  TRACE_POP
}
extern void DutMonitor_eqFunction_13(DATA *data, threadData_t *threadData);

extern void DutMonitor_eqFunction_14(DATA *data, threadData_t *threadData);

extern void DutMonitor_eqFunction_15(DATA *data, threadData_t *threadData);

extern void DutMonitor_eqFunction_11(DATA *data, threadData_t *threadData);

OMC_DISABLE_OPT
void DutMonitor_functionInitialEquations_0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  DutMonitor_eqFunction_1(data, threadData);
  DutMonitor_eqFunction_10(data, threadData);
  DutMonitor_eqFunction_3(data, threadData);
  DutMonitor_eqFunction_4(data, threadData);
  DutMonitor_eqFunction_13(data, threadData);
  DutMonitor_eqFunction_14(data, threadData);
  DutMonitor_eqFunction_15(data, threadData);
  DutMonitor_eqFunction_11(data, threadData);
  TRACE_POP
}

int DutMonitor_functionInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->discreteCall = 1;
  DutMonitor_functionInitialEquations_0(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
  TRACE_POP
  return 0;
}

/* No DutMonitor_functionInitialEquations_lambda0 function */

int DutMonitor_functionRemovedInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int *equationIndexes = NULL;
  double res = 0.0;

  
  TRACE_POP
  return 0;
}


#if defined(__cplusplus)
}
#endif

