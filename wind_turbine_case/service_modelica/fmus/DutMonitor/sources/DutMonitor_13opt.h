#if defined(__cplusplus)
  extern "C" {
#endif
  int DutMonitor_mayer(DATA* data, modelica_real** res, short*);
  int DutMonitor_lagrange(DATA* data, modelica_real** res, short *, short *);
  int DutMonitor_pickUpBoundsForInputsInOptimization(DATA* data, modelica_real* min, modelica_real* max, modelica_real*nominal, modelica_boolean *useNominal, char ** name, modelica_real * start, modelica_real * startTimeOpt);
  int DutMonitor_setInputData(DATA *data, const modelica_boolean file);
  int DutMonitor_getTimeGrid(DATA *data, modelica_integer * nsi, modelica_real**t);
#if defined(__cplusplus)
}
#endif