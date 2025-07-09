model SetInput
  parameter Real k=1.0;
  Modelica.Blocks.Sources.Constant test_bench_set_speed(k = k) annotation(
    Placement(visible = true, transformation(origin = {-18, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(visible = true, transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(test_bench_set_speed.y, y) annotation(
    Line(points = {{-7, 0}, {110, 0}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end SetInput;
