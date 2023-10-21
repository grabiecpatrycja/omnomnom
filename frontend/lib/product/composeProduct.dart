import 'dart:collection';
import 'dart:convert';

import 'package:calcounter/http/nutrition.dart';
import 'package:calcounter/http/product.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart';

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
  final HashMap<int, double> values = HashMap();

  final controller = TextEditingController();
  late String newProductName;

  int index = 0;

  @override
  void initState() {
    super.initState();
    nutritions = NutritionService.fetchNutritions();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(future: nutritions, builder: (context, snapshot) {
      if (snapshot.hasData) {
        TextEditingController tec = TextEditingController();
        Step productNameInput = Step(
            title: const Text('Name of the new product'),
            content: TextField(controller: tec, onChanged: (String text) {
              newProductName = tec.text;
            })
        );

        List<Step> steps = snapshot.data!.map((Nutrition nutrition) {
          return Step(
            title: Text(nutrition.name),
            content: TextField(
                controller: controller, onChanged: (String text) {
              double? value = double.tryParse(text);
              if (value != null) {
                values[nutrition.id] = value;
              }
            }),
          );
        }).toList();
        steps.insert(0, productNameInput);

        return Stepper(
          currentStep: index,
          onStepContinue: () async {
            if (index == steps.length - 1) {
              Response response = await ProductService.addProduct(newProductName);
              int productId = jsonDecode(response.body)['id'];
              ProductService.addNutritionsToProduct(productId, values);
              context.goNamed('products');
            }
            else {
              setState(() {
                controller.clear();
                index += 1;
              });
            }
          },
          onStepCancel: () {
            context.goNamed('main');
          },
          steps: steps,
        );
      }
        return const Text('Loading...');
    });
  }

}