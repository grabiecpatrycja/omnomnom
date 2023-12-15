import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class MainChart extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BarChart(
        BarChartData(
            barGroups: [
              BarChartGroupData(
                  x: 0,
                  barRods: [
                    BarChartRodData(toY: 10)
                  ]
              ),
              BarChartGroupData(
                  x: 10,
                  barRods: [
                    BarChartRodData(toY: 20)
                  ]
              )
            ]
        )
    );
  }

}