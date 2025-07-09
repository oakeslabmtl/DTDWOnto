/* Algebraic */
#include "DutMonitor_model.h"

#ifdef __cplusplus
extern "C" {
#endif


/* forwarded equations */
extern void DutMonitor_eqFunction_9(DATA* data, threadData_t *threadData);
extern void DutMonitor_eqFunction_10(DATA* data, threadData_t *threadData);
extern void DutMonitor_eqFunction_11(DATA* data, threadData_t *threadData);
extern void DutMonitor_eqFunction_12(DATA* data, threadData_t *threadData);
extern void DutMonitor_eqFunction_13(DATA* data, threadData_t *threadData);
extern void DutMonitor_eqFunction_14(DATA* data, threadData_t *threadData);
extern void DutMonitor_eqFunction_15(DATA* data, threadData_t *threadData);

static void functionAlg_system0(DATA *data, threadData_t *threadData)
{
  {
    DutMonitor_eqFunction_9(data, threadData);
    threadData->lastEquationSolved = 9;
  }
  {
    DutMonitor_eqFunction_10(data, threadData);
    threadData->lastEquationSolved = 10;
  }
  {
    DutMonitor_eqFunction_11(data, threadData);
    threadData->lastEquationSolved = 11;
  }
  {
    DutMonitor_eqFunction_12(data, threadData);
    threadData->lastEquationSolved = 12;
  }
  {
    DutMonitor_eqFunction_13(data, threadData);
    threadData->lastEquationSolved = 13;
  }
  {
    DutMonitor_eqFunction_14(data, threadData);
    threadData->lastEquationSolved = 14;
  }
  {
    DutMonitor_eqFunction_15(data, threadData);
    threadData->lastEquationSolved = 15;
  }
}
/* for continuous time variables */
int DutMonitor_functionAlgebraics(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_ALGEBRAICS);
#endif
  data->simulationInfo->callStatistics.functionAlgebraics++;

  DutMonitor_function_savePreSynchronous(data, threadData);
  
  functionAlg_system0(data, threadData);

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_ALGEBRAICS);
#endif

  TRACE_POP
  return 0;
}

#ifdef __cplusplus
}
#endif
