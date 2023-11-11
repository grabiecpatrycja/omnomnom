import 'package:calcounter/container/models.dart';
import 'package:calcounter/http/container.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart' as http;


class ContainerInsidesWidget extends StatefulWidget {
  final int id;
  const ContainerInsidesWidget({required this.id, super.key});

  @override
  State<StatefulWidget> createState() {
    return ContainerInsidesState(id: id);
  }

}


class ContainerInsidesState extends State<ContainerInsidesWidget> {
  final int id;
  late Future<OContainer> containerResponse;
  ContainerInsidesState({required this.id});

  @override
  void initState() {
    super.initState();
    containerResponse = ContainerService.fetchContainer(id);
  }

  Widget build(BuildContext context) {
    return FutureBuilder(future: containerResponse, builder: (context, snapshot)
    {
      if (!snapshot.hasData) {
        return const Text('Loading...');
      }

      final data = snapshot.data!;
      return Table(
        columnWidths: const <int, TableColumnWidth>{
          0: IntrinsicColumnWidth(),
          1: IntrinsicColumnWidth(),
          2: FixedColumnWidth(50),
        },
        children: data.products!.entries.map((product_entry) {
          return TableRow(children: [
            Text(product_entry.key as String),
            Text(product_entry.value.toString()),
            const Text(''),
          ]);
        }).toList(),
      );
    });
  }

}


class ContainerCheckinWidget extends StatelessWidget {
  final TextEditingController controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return MaterialButton(onPressed: () {
      showDialog(context: context, builder: (context) {
        return AlertDialog(
          title: const Text('Weight'),
          content: TextField(
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
              ),
              controller: controller
          ),
          actions: [
            TextButton(
              onPressed: () {
                debugPrint(controller.text);
              },
              child: const Text('OK'),
            ),
            TextButton(
              onPressed: () {
                GoRouter.of(context).pop();
              },
              child: const Text('Cancel'),
            )
          ]
        );
      });
    }, child: const SizedBox(
      width: 100,
      height: 100,
      child: ColoredBox(color: Colors.redAccent, child: Center(child: Text(('WEIGHT IT!!1!')))),
    ));
  }
}



class ContainerDetailWidget extends StatelessWidget {
  final int id;
  const ContainerDetailWidget({required this.id, super.key});

  Widget build(BuildContext context) {
    return Column(children: [
      ContainerCheckinWidget(),
      MaterialButton(onPressed: () {
        GoRouter.of(context).pop();
      }, child: const Text('Back')),
      ContainerInsidesWidget(id: id),
    ]);
  }

}