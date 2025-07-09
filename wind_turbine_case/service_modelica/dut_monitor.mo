model DutMonitor
  Modelica.Mechanics.Rotational.Components.Inertia dut_turbine(J = 1, a(start = 0), phi(displayUnit = "rad", start = 0), stateSelect = StateSelect.always, w(start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-36, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_set_torque annotation(
    Placement(visible = true, transformation(origin = {-100, 80}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.AngleToTorqueAdaptor angleToTorqueAdaptor annotation(
    Placement(visible = true, transformation(origin = {-56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_angle annotation(
    Placement(visible = true, transformation(origin = {-100, 56}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 10}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_speed annotation(
    Placement(visible = true, transformation(origin = {-100, 32}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_acceleration annotation(
    Placement(visible = true, transformation(origin = {-100, 8}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, -80}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.TorqueToAngleAdaptor coupling(use_a = true, use_w = true)  annotation(
    Placement(visible = true, transformation(origin = {-16, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput dut_out_angle annotation(
    Placement(visible = true, transformation(origin = {-100, -18}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-110, -70}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput dut_out_speed annotation(
    Placement(visible = true, transformation(origin = {-100, -44}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-100, -60}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput dut_out_acceleration annotation(
    Placement(visible = true, transformation(origin = {-100, -68}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-90, -50}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput dut_out_torque annotation(
    Placement(visible = true, transformation(origin = {-100, -90}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-80, -40}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Math.Add add(k1 = -1)  annotation(
    Placement(visible = true, transformation(origin = {54, -38}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_conformance annotation(
    Placement(visible = true, transformation(origin = {110, -38}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {82, -6}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(in_acceleration, angleToTorqueAdaptor.a) annotation(
    Line(points = {{-100, 8}, {-80, 8}, {-80, 2}, {-58, 2}}, color = {0, 0, 127}));
  connect(in_speed, angleToTorqueAdaptor.w) annotation(
    Line(points = {{-100, 32}, {-79, 32}, {-79, 6}, {-58, 6}}, color = {0, 0, 127}));
  connect(in_angle, angleToTorqueAdaptor.phi) annotation(
    Line(points = {{-100, 56}, {-66, 56}, {-66, 8}, {-58, 8}}, color = {0, 0, 127}));
  connect(angleToTorqueAdaptor.flange, dut_turbine.flange_a) annotation(
    Line(points = {{-54, 0}, {-46, 0}}));
  connect(dut_turbine.flange_b, coupling.flange) annotation(
    Line(points = {{-26, 0}, {-18, 0}}));
  connect(in_set_torque, coupling.tau) annotation(
    Line(points = {{-100, 80}, {54, 80}, {54, -8}, {-13, -8}}, color = {0, 0, 127}));
  connect(coupling.w, add.u1) annotation(
    Line(points = {{-12, 6}, {42, 6}, {42, -32}}, color = {0, 0, 127}));
  connect(dut_out_speed, add.u2) annotation(
    Line(points = {{-100, -44}, {42, -44}}, color = {0, 0, 127}));
  connect(add.y, out_conformance) annotation(
    Line(points = {{66, -38}, {110, -38}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end DutMonitor;
