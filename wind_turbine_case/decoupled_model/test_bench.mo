model TestBench
  Modelica.Mechanics.Rotational.Components.Inertia testbench_inertia(J = 1, a(start = 0), phi(displayUnit = "rad", start = 0), stateSelect = StateSelect.always, w(start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-20, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.SpringDamper testbench_coupling(a_rel(start = 0),c = 1, d = 1, phi_nominal = 1, phi_rel(start = 0), phi_rel0 = 0, stateSelect = StateSelect.avoid, w_rel(start = 0))  annotation(
    Placement(visible = true, transformation(origin = {16, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.PI test_bench_ctrl(T = 1, initType = Modelica.Blocks.Types.Init.NoInit, k = 1, x(fixed = true, start = 0), x_start = 0, y_start = 0)  annotation(
    Placement(visible = true, transformation(origin = {-78, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sources.Torque test_bench_torque annotation(
    Placement(visible = true, transformation(origin = {-48, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sensors.SpeedSensor test_bench_speed_sensor annotation(
    Placement(visible = true, transformation(origin = {-10, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Blocks.Math.Feedback test_bench_feedback annotation(
    Placement(visible = true, transformation(origin = {-90, 44}, extent = {{-10, 10}, {10, -10}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealInput in_set_speed annotation(
    Placement(visible = true, transformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 60}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.TorqueToAngleAdaptor coupling annotation(
    Placement(visible = true, transformation(origin = {42, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_angle annotation(
    Placement(visible = true, transformation(origin = {110, 52}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 70}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_speed annotation(
    Placement(visible = true, transformation(origin = {110, 26}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_acceleration annotation(
    Placement(visible = true, transformation(origin = {110, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, -50}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput in_torque annotation(
    Placement(visible = true, transformation(origin = {-120, -30}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, -60}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput out_angle_inertia annotation(
    Placement(visible = true, transformation(origin = {110, 82}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, -86}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sensors.AngleSensor angle_sensor annotation(
    Placement(visible = true, transformation(origin = {10, 82}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(testbench_inertia.flange_b, testbench_coupling.flange_a) annotation(
    Line(points = {{-10, 0}, {6, 0}}));
  connect(test_bench_torque.flange, testbench_inertia.flange_a) annotation(
    Line(points = {{-38, 0}, {-30, 0}}));
  connect(test_bench_ctrl.y, test_bench_torque.tau) annotation(
    Line(points = {{-67, 0}, {-60, 0}}, color = {0, 0, 127}));
  connect(testbench_inertia.flange_b, test_bench_speed_sensor.flange) annotation(
    Line(points = {{-10, 0}, {-10, 22}}));
  connect(test_bench_speed_sensor.w, test_bench_feedback.u2) annotation(
    Line(points = {{-10, 44}, {-82, 44}}, color = {0, 0, 127}));
  connect(test_bench_feedback.y, test_bench_ctrl.u) annotation(
    Line(points = {{-90, 35}, {-90, 0}}, color = {0, 0, 127}));
  connect(in_set_speed, test_bench_feedback.u1) annotation(
    Line(points = {{-120, 60}, {-105, 60}, {-105, 52}, {-90, 52}}, color = {0, 0, 127}));
  connect(testbench_coupling.flange_b, coupling.flange) annotation(
    Line(points = {{26, 0}, {40, 0}}));
  connect(coupling.phi, out_angle) annotation(
    Line(points = {{46, 8}, {70, 8}, {70, 52}, {110, 52}}, color = {0, 0, 127}));
  connect(in_torque, coupling.tau) annotation(
    Line(points = {{-120, -30}, {60, -30}, {60, -8}, {46, -8}}, color = {0, 0, 127}));
  connect(coupling.w, out_speed) annotation(
    Line(points = {{46, 6}, {80, 6}, {80, 26}, {110, 26}}, color = {0, 0, 127}));
  connect(coupling.a, out_acceleration) annotation(
    Line(points = {{46, 2}, {110, 2}}, color = {0, 0, 127}));
  connect(testbench_inertia.flange_b, angle_sensor.flange) annotation(
    Line(points = {{-10, 0}, {-4, 0}, {-4, 20}, {0, 20}, {0, 82}}));
  connect(angle_sensor.phi, out_angle_inertia) annotation(
    Line(points = {{21, 82}, {110, 82}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end TestBench;
