model coupled_model_adaptors_full
  Modelica.Mechanics.Rotational.Components.Inertia testbench_inertia(J = 1, a(start = 0), phi(displayUnit = "rad", start = 0), stateSelect = StateSelect.prefer, w(start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-20, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.SpringDamper testbench_coupling(a_rel(start = 0),c = 1, d = 1, phi_nominal = 1, phi_rel(start = 0), phi_rel0 = 0, stateSelect = StateSelect.never, w_rel(start = 0))  annotation(
    Placement(visible = true, transformation(origin = {10, -16}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.Inertia dut_turbine(J = 1, a(start = 0), phi(displayUnit = "rad", start = 0), stateSelect = StateSelect.prefer, w(start = 0))  annotation(
    Placement(visible = true, transformation(origin = {46, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.PI test_bench_ctrl(T = 1, initType = Modelica.Blocks.Types.Init.NoInit, k = 1, x(fixed = true, start = 0), x_start = 0, y_start = 0)  annotation(
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
  Modelica.Mechanics.Rotational.Components.TorqueToAngleAdaptor test_bench_adaptor(use_a = true, use_w = true)  annotation(
    Placement(visible = true, transformation(origin = {20, -56}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.AngleToTorqueAdaptor dut_adaptor annotation(
    Placement(visible = true, transformation(origin = {52, -56}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.TorqueToAngleAdaptor dut_torque_in(use_a = true, use_w = true) annotation(
    Placement(visible = true, transformation(origin = {74, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(testbench_inertia.flange_b, testbench_coupling.flange_a) annotation(
    Line(points = {{-10, 0}, {-5, 0}, {-5, -16}, {0, -16}}));
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
  connect(testbench_coupling.flange_b, test_bench_adaptor.flange) annotation(
    Line(points = {{20, -16}, {26, -16}, {26, -36}, {-2, -36}, {-2, -56}, {18, -56}}));
  connect(test_bench_adaptor.phi, dut_adaptor.phi) annotation(
    Line(points = {{24, -48}, {50, -48}}, color = {0, 0, 127}));
  connect(test_bench_adaptor.a, dut_adaptor.a) annotation(
    Line(points = {{24, -54}, {50, -54}}, color = {0, 0, 127}));
  connect(dut_adaptor.tau, test_bench_adaptor.tau) annotation(
    Line(points = {{50, -64}, {24, -64}}, color = {0, 0, 127}));
  connect(dut_adaptor.flange, dut_turbine.flange_a) annotation(
    Line(points = {{54, -56}, {64, -56}, {64, -28}, {36, -28}, {36, 0}}));
  connect(test_bench_adaptor.w, dut_adaptor.w) annotation(
    Line(points = {{24, -50}, {50, -50}}, color = {0, 0, 127}));
  connect(dut_turbine.flange_b, dut_torque_in.flange) annotation(
    Line(points = {{56, 0}, {72, 0}}));
  connect(dut_set_torque.y, dut_torque_in.tau) annotation(
    Line(points = {{84, 74}, {84, -8}, {78, -8}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")),
    experiment(StartTime = 0, StopTime = 50, Tolerance = 1e-6, Interval = 0.1));
end coupled_model_adaptors_full;
