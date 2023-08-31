import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'nutrition.dart' as model;

Future<List<model.Nutrition>> fetchNutritions() async {
  final response = await http.get(Uri.parse('http://localhost:8000/api/nutritions'));
  final data = jsonDecode(response.body);
  List<model.Nutrition> nutritions = [];

  for (final entry in data) {
    nutritions.add(model.Nutrition(name: entry['name'], id: entry['id']));
  }
  return nutritions;
}

class NutritionsWidget extends StatefulWidget {
  const NutritionsWidget({super.key});

  @override
  State<StatefulWidget> createState() {
    return NutritionsWidgetState();
  }

}


class NutritionsWidgetState extends State<NutritionsWidget> {
  List<model.Nutrition> nutritions = [];
  late Future<List<model.Nutrition>> nutritionsResponse;

  @override
  void initState() {
    super.initState();
    nutritionsResponse = fetchNutritions();
  }

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      Spacer(),
      Expanded(child: Text('These are the nutritions you want to keep track of')),
      FutureBuilder(future: nutritionsResponse, builder: (context, snapshot) {
        if (snapshot.hasData) {
          List<Widget> buttons = snapshot.data!.map((e) {
            ElevatedButton the_button = ElevatedButton(child: Text(e.name), onPressed: null,);
            // return Row(children: [the_button], mainAxisAlignment: MainAxisAlignment.center,);
            return the_button;
          }).toList();

          return Column(children:
          [
            Row(children: buttons, mainAxisAlignment: MainAxisAlignment.center,),
            SizedBox(height: 10,),
            ElevatedButton(child: Text('+'), onPressed: null,),
          ],
              mainAxisAlignment: MainAxisAlignment.center);
        }
        else {
          return Text('Downloading');
        }
      }),
      Spacer(),
    ]);
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