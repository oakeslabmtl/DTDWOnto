model Dut
  Modelica.Mechanics.Rotational.Components.Inertia dut_turbine(J = 1, a(start = 0), phi(displayUnit = "rad", start = 0), stateSelect = StateSelect.always, w(start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-14, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_set_torque annotation(
    Placement(visible = true, transformation(origin = {-100, 80}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.AngleToTorqueAdaptor angleToTorqueAdaptor annotation(
    Placement(visible = true, transformation(origin = {-56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_angle annotation(
    Placement(visible = true, transformation(origin = {-100, 30}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 10}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_speed annotation(
    Placement(visible = true, transformation(origin = {-100, -6}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, -36}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_acceleration annotation(
    Placement(visible = true, transformation(origin = {-100, -44}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, -80}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_torque annotation(
    Placement(visible = true, transformation(origin = {110, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, -78}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_speed annotation(
    Placement(visible = true, transformation(origin = {110, -20}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_angle annotation(
    Placement(visible = true, transformation(origin = {110, -4}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.TorqueToAngleAdaptor coupling(use_a = true, use_w = true)  annotation(
    Placement(visible = true, transformation(origin = {40, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_acceleration annotation(
    Placement(visible = true, transformation(origin = {110, -42}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(angleToTorqueAdaptor.tau, out_torque) annotation(
    Line(points = {{-58, -8}, {-62, -8}, {-62, -80}, {110, -80}}, color = {0, 0, 127}));
  connect(in_acceleration, angleToTorqueAdaptor.a) annotation(
    Line(points = {{-100, -44}, {-74, -44}, {-74, 2}, {-58, 2}}, color = {0, 0, 127}));
  connect(in_speed, angleToTorqueAdaptor.w) annotation(
    Line(points = {{-100, -6}, {-76, -6}, {-76, 6}, {-58, 6}}, color = {0, 0, 127}));
  connect(in_angle, angleToTorqueAdaptor.phi) annotation(
    Line(points = {{-100, 30}, {-66, 30}, {-66, 8}, {-58, 8}}, color = {0, 0, 127}));
  connect(angleToTorqueAdaptor.flange, dut_turbine.flange_a) annotation(
    Line(points = {{-54, 0}, {-24, 0}}));
  connect(dut_turbine.flange_b, coupling.flange) annotation(
    Line(points = {{-4, 0}, {38, 0}}));
  connect(coupling.w, out_speed) annotation(
    Line(points = {{44, 6}, {82, 6}, {82, -20}, {110, -20}}, color = {0, 0, 127}));
  connect(in_set_torque, coupling.tau) annotation(
    Line(points = {{-100, 80}, {54, 80}, {54, -8}, {44, -8}}, color = {0, 0, 127}));
  connect(coupling.a, out_acceleration) annotation(
    Line(points = {{44, 2}, {72, 2}, {72, -42}, {110, -42}}, color = {0, 0, 127}));
  connect(coupling.phi, out_angle) annotation(
    Line(points = {{44, 8}, {86, 8}, {86, -4}, {110, -4}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end Dut;
