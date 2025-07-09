model coupled_model_tortion
  Modelica.Mechanics.Rotational.Components.Inertia testbench_inertia(J = 1)  annotation(
    Placement(visible = true, transformation(origin = {-20, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.SpringDamper testbench_coupling(c = 1, d = 1)  annotation(
    Placement(visible = true, transformation(origin = {6, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.Inertia dut_turbine(J = 1)  annotation(
    Placement(visible = true, transformation(origin = {42, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.PI test_bench_ctrl(k = 1)  annotation(
    Placement(visible = true, transformation(origin = {-78, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sources.Torque test_bench_torque annotation(
    Placement(visible = true, transformation(origin = {-48, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant test_bench_set_speed(k = 1)  annotation(
    Placement(visible = true, transformation(origin = {-88, 84}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Mechanics.Rotational.Sensors.SpeedSensor test_bench_speed_sensor annotation(
    Placement(visible = true, transformation(origin = {-10, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 90)));
  Modelica.Blocks.Math.Feedback test_bench_feedback annotation(
    Placement(visible = true, transformation(origin = {-90, 44}, extent = {{-10, 10}, {10, -10}}, rotation = -90)));
  Modelica.Blocks.Sources.Constant dut_set_torque(k = -1) annotation(
    Placement(visible = true, transformation(origin = {84, 84}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Mechanics.Rotational.Sources.Torque dut_torque_ctrl annotation(
    Placement(visible = true, transformation(origin = {72, 0}, extent = {{10, -10}, {-10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sensors.RelAngleSensor tortion_sensor annotation(
    Placement(visible = true, transformation(origin = {22, 62}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
equation
  connect(testbench_inertia.flange_b, testbench_coupling.flange_a) annotation(
    Line(points = {{-10, 0}, {-4, 0}}));
  connect(testbench_coupling.flange_b, dut_turbine.flange_a) annotation(
    Line(points = {{16, 0}, {32, 0}}));
  connect(test_bench_torque.flange, testbench_inertia.flange_a) annotation(
    Line(points = {{-38, 0}, {-30, 0}}));
  connect(test_bench_ctrl.y, test_bench_torque.tau) annotation(
    Line(points = {{-67, 0}, {-60, 0}}, color = {0, 0, 127}));
  connect(testbench_inertia.flange_b, test_bench_speed_sensor.flange) annotation(
    Line(points = {{-10, 0}, {-10, 22}}));
  connect(test_bench_set_speed.y, test_bench_feedback.u1) annotation(
    Line(points = {{-88, 73}, {-88, 62.5}, {-90, 62.5}, {-90, 52}}, color = {0, 0, 127}));
  connect(test_bench_speed_sensor.w, test_bench_feedback.u2) annotation(
    Line(points = {{-10, 44}, {-82, 44}}, color = {0, 0, 127}));
  connect(test_bench_feedback.y, test_bench_ctrl.u) annotation(
    Line(points = {{-90, 35}, {-90, 0}}, color = {0, 0, 127}));
  connect(dut_turbine.flange_b, dut_torque_ctrl.flange) annotation(
    Line(points = {{52, 0}, {62, 0}}));
  connect(dut_set_torque.y, dut_torque_ctrl.tau) annotation(
    Line(points = {{84, 73}, {84, 0}}, color = {0, 0, 127}));
  connect(tortion_sensor.flange_a, dut_turbine.flange_b) annotation(
    Line(points = {{32, 62}, {52, 62}, {52, 0}}));
  connect(tortion_sensor.flange_b, testbench_inertia.flange_a) annotation(
    Line(points = {{12, 62}, {-30, 62}, {-30, 0}}));
  annotation(
    uses(Modelica(version = "4.0.0")),
    experiment(StartTime = 0, StopTime = 50, Tolerance = 1e-6, Interval = 0.1));
end coupled_model_tortion;
