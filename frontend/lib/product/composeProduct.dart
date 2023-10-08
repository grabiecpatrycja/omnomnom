import 'package:calcounter/http/nutrition.dart';
import 'package:flutter/material.dart';

import '../nutrition.dart';

class ComposeProduct extends StatefulWidget {
  const ComposeProduct({super.key});

  @override
  State<StatefulWidget> createState() {
    return ComposeProductState();
  }

}


class ComposeProductState extends State<ComposeProduct> {
  late Future<List<Nutrition>> nutritions;
  int index = 0;

  @override
  void initState() {
    super.initState();
    nutritions = NutritionService.fetchNutritions();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(future: nutritions, builder: (context, snapshop) {
      return Stepper(
          currentStep: index,
          onStepContinue: () {
            setState(() {
              index += 1;
            });
          },
          steps: const <Step>[
            Step(
                title: Text('some1'),
                content: Text('some1 content')
            ),
            Step(
                title: Text('asdf'),
                content: Text('asdf'))
          ]);
    });
  }

}