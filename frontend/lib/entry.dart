import 'package:calcounter/http/nutrition.dart';
import 'package:flutter/material.dart';

class NutritionEntry extends StatelessWidget {
  final String name;
  final int id;
  final VoidCallback refresh;

  const NutritionEntry(this.id, this.name, this.refresh, {super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(4.0),
        child: MaterialButton(
          onPressed: () {
            showDialog(
                context: context,
                builder: (context) {
                  return AlertDialog(
                    title: const Text('Nutrition deletion'),
                    content: const Text('Confirm nutrition deletion'),
                    actions: [
                      TextButton(onPressed: () {
                        NutritionService.deleteNutrition(id).then((response) {
                          refresh();
                          Navigator.pop(context);
                        });
                      }, child: const Text('Delete'))
                    ],
                  );
                });
          },
          color: Colors.green,
          textColor: Colors.white,
          child: Text(name),
          hoverColor: Colors.red,
        )
    );
  }

}