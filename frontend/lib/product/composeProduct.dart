import 'package:flutter/material.dart';

import '../nutrition.dart';

class ComposeProduct extends StatefulWidget {
  final List<Nutrition> nutritions;

  const ComposeProduct({super.key, required this.nutritions});

  @override
  State<StatefulWidget> createState() {
    return ComposeProductState(nutritions: nutritions);
  }

}


class ComposeProductState extends State<ComposeProduct> {
  final List<Nutrition> nutritions;
  int index = 0;

  ComposeProductState({required this.nutritions});

  @override
  Widget build(BuildContext context) {
    Material()
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
  }

}