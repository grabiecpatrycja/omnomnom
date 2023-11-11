import 'package:calcounter/http/container.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'models.dart';


class NewContainerButton extends StatelessWidget {
  final nameController = TextEditingController();
  
  Widget build(BuildContext context) {
    return MaterialButton(onPressed: () {
      showDialog(context: context, builder: (context) {
        return AlertDialog(
          title: const Text('Compose a container'),
          content: TextField(
            controller: nameController,
            decoration: InputDecoration(
              border: OutlineInputBorder()
            )
          ),
          actions: <Widget>[
            TextButton(onPressed: () => GoRouter.of(context).pop(), child: const Text('Cancel')),
            TextButton(onPressed: () => print(nameController.text), child: const Text('Create')),
          ]
        );
      });
    }, child: const Text('Compose a new container'));
  }

}


class OContainerWidget extends StatelessWidget {
  final String name;
  final int id;
  const OContainerWidget({required this.name, required this.id, super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      color: Theme.of(context).colorScheme.surfaceVariant,
      clipBehavior: Clip.hardEdge,
      child: InkWell(
        splashColor: Colors.blue.withAlpha(30),
        onTap: () {
          GoRouter.of(context).goNamed('containerDetail', pathParameters: {'containerId': id.toString()});
        },
        child: SizedBox(
          width: 300,
          height: 100,
            child: Center(child: Text(name)),
        )
      )
    );
  }
}


class OContainers extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return OContainersState();
  }

}

class OContainersState extends State<OContainers> {
  late Future<List<OContainer>> fetchContainers;

  @override
  void initState(){
    super.initState();
    fetchContainers = ContainerService.fetchContainers();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(future: fetchContainers, builder: (context, snapshot) {
      if (snapshot.connectionState != ConnectionState.done) {
        return const Text('Loading...');
      }

      final containers = snapshot.data!;
      return Column(children: <Widget>[
        GridView.count(
            shrinkWrap: true,
            crossAxisCount: 3,
            children: containers.map<Widget>((e) {
              return OContainerWidget(name: e.name, id: e.id!);
            }).toList()
        ),
        const Divider(),
        NewContainerButton(),
      ]
      );
    });
  }
}