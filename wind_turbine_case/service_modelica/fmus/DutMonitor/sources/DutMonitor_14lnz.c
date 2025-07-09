/* Linearization */
#include "DutMonitor_model.h"
#if defined(__cplusplus)
extern "C" {
#endif
const char *DutMonitor_linear_model_frame()
{
  return "model linearized_model \"DutMonitor\" \n  parameter Integer n = 0 \"number of states\";\n  parameter Integer m = 8 \"number of inputs\";\n  parameter Integer p = 1 \"number of outputs\";\n"
  "  parameter Real x0[n] = %s;\n"
  "  parameter Real u0[m] = %s;\n"
  "\n"
  "  parameter Real A[n, n] = zeros(n, n);%s\n\n"
  "  parameter Real B[n, m] = zeros(n, m);%s\n\n"
  "  parameter Real C[p, n] = zeros(p, n);%s\n\n"
  "  parameter Real D[p, m] =\n\t[%s];\n\n"
  "\n"
  "  Real x[n];\n"
  "  input Real u[m](start=u0);\n"
  "  output Real y[p];\n"
  "\n"
  "  Real 'u_dut_out_acceleration' = u[1];\n""  Real 'u_dut_out_angle' = u[2];\n""  Real 'u_dut_out_speed' = u[3];\n""  Real 'u_dut_out_torque' = u[4];\n""  Real 'u_in_acceleration' = u[5];\n""  Real 'u_in_angle' = u[6];\n""  Real 'u_in_set_torque' = u[7];\n""  Real 'u_in_speed' = u[8];\n"
  "  Real 'y_out_conformance' = y[1];\n"
  "equation\n  der(x) = A * x + B * u;\n  y = C * x + D * u;\nend linearized_model;\n";
}
const char *DutMonitor_linear_model_datarecovery_frame()
{
  return "model linearized_model \"DutMonitor\" \n parameter Integer n = 0 \"number of states\";\n  parameter Integer m = 8 \"number of inputs\";\n  parameter Integer p = 1 \"number of outputs\";\n  parameter Integer nz = 16 \"data recovery variables\";\n"
  "  parameter Real x0[0] = %s;\n"
  "  parameter Real u0[8] = %s;\n"
  "  parameter Real z0[16] = %s;\n"
  "\n"
  "  parameter Real A[n, n] = zeros(n, n);%s\n\n"
  "  parameter Real B[n, m] = zeros(n, m);%s\n\n"
  "  parameter Real C[p, n] = zeros(p, n);%s\n\n"
  "  parameter Real D[p, m] =\n\t[%s];\n\n"
  "  parameter Real Cz[nz, n] = zeros(nz, n);%s\n\n"
  "  parameter Real Dz[nz, m] =\n\t[%s];\n\n"
  "\n"
  "  Real x[n];\n"
  "  input Real u[m](start=u0);\n"
  "  output Real y[p];\n"
  "  output Real z[nz];\n"
  "\n"
  "  Real 'u_dut_out_acceleration' = u[1];\n""  Real 'u_dut_out_angle' = u[2];\n""  Real 'u_dut_out_speed' = u[3];\n""  Real 'u_dut_out_torque' = u[4];\n""  Real 'u_in_acceleration' = u[5];\n""  Real 'u_in_angle' = u[6];\n""  Real 'u_in_set_torque' = u[7];\n""  Real 'u_in_speed' = u[8];\n"
  "  Real 'y_out_conformance' = y[1];\n"
  "  Real 'z_der(dut_turbine.phi)' = z[1];\n""  Real 'z_der(dut_turbine.w)' = z[2];\n""  Real 'z_angleToTorqueAdaptor.move.phi_support' = z[3];\n""  Real 'z_angleToTorqueAdaptor.tau' = z[4];\n""  Real 'z_dut_out_acceleration' = z[5];\n""  Real 'z_dut_out_angle' = z[6];\n""  Real 'z_dut_out_speed' = z[7];\n""  Real 'z_dut_out_torque' = z[8];\n""  Real 'z_dut_turbine.a' = z[9];\n""  Real 'z_dut_turbine.phi' = z[10];\n""  Real 'z_dut_turbine.w' = z[11];\n""  Real 'z_in_acceleration' = z[12];\n""  Real 'z_in_angle' = z[13];\n""  Real 'z_in_set_torque' = z[14];\n""  Real 'z_in_speed' = z[15];\n""  Real 'z_out_conformance' = z[16];\n"
  "equation\n  der(x) = A * x + B * u;\n  y = C * x + D * u;\n  z = Cz * x + Dz * u;\nend linearized_model;\n";
}
#if defined(__cplusplus)
}
#endif

