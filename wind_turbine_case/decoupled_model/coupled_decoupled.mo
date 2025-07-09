model coupled_decoupled
  Modelica.Blocks.Sources.Constant dut_set_torque(k = -1) annotation(
    Placement(visible = true, transformation(origin = {0, 50}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Dut dut annotation(
    Placement(visible = true, transformation(origin = {22, 8}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  TestBench testBench annotation(
    Placement(visible = true, transformation(origin = {-48, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant test_bench_set_speed(k = 1) annotation(
    Placement(visible = true, transformation(origin = {-80, 50}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
equation
  connect(dut_set_torque.y, dut.in_set_torque) annotation(
    Line(points = {{0, 39}, {0, 14}, {10, 14}}, color = {0, 0, 127}));
  connect(testBench.out_angle, dut.in_angle) annotation(
    Line(points = {{-36, 10}, {10, 10}, {10, 9}}, color = {0, 0, 127}));
  connect(testBench.out_speed, dut.in_speed) annotation(
    Line(points = {{-36, 4}, {10, 4}}, color = {0, 0, 127}));
  connect(testBench.out_acceleration, dut.in_acceleration) annotation(
    Line(points = {{-36, -2}, {-14, -2}, {-14, 0}, {10, 0}}, color = {0, 0, 127}));
  connect(test_bench_set_speed.y, testBench.in_set_speed) annotation(
    Line(points = {{-80, 39}, {-80, 8}, {-60, 8}}, color = {0, 0, 127}));
  connect(dut.out_torque, testBench.in_torque) annotation(
    Line(points = {{33, 0}, {40, 0}, {40, -20}, {-80, -20}, {-80, -4}, {-60, -4}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")),
    experiment(StartTime = 0, StopTime = 50, Tolerance = 1e-6, Interval = 0.1));
end coupled_decoupled;
