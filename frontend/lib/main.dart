import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'nutrition.dart' as model;

class NutritionsWidget extends StatefulWidget {
  const NutritionsWidget({super.key});

  @override
  State<StatefulWidget> createState() {
    return NutritionsWidgetState();
  }

}


class NutritionsWidgetState extends State<NutritionsWidget> {
  List<model.Nutrition> nutritions = [];

  @override
  void initState() {
    super.initState();
  }

  Widget build(BuildContext context) {
    return const Row(
      children: [
        SizedBox(width: 16),
        ElevatedButton(onPressed: null, child: Text('Download')),
      ],
    );
  }

}

class MyScaffold extends StatelessWidget {
  const MyScaffold({super.key});

  @override
  Widget build(BuildContext context) {
    return const Material(
            child: NutritionsWidget()
    );
  }
}

void main() {
  runApp(
    const MaterialApp(
      title: 'My app', // used by the OS task switcher
      home: SafeArea(
        child: MyScaffold(),
      ),
    ),
  );
}