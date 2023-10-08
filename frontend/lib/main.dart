import 'dart:convert';

import 'package:calcounter/entry.dart';
import 'package:calcounter/http/nutrition.dart';
import 'package:calcounter/product/composeProduct.dart';
import 'package:calcounter/product/main.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
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
  late Future<List<model.Nutrition>> nutritionsResponse;
  final textController = TextEditingController();

  @override
  void initState() {
    super.initState();
    nutritionsResponse = NutritionService.fetchNutritions();
  }


  @override
  Widget build(BuildContext context) {
    var that = this;
    return Column(children: [
      Spacer(),
      Expanded(child: Text('These are the nutritions you want to keep track of')),
      FutureBuilder(future: nutritionsResponse, builder: (context, snapshot) {
        if (snapshot.hasData) {
          List<Widget> buttons = snapshot.data!.map((e) {
            Widget the_button = NutritionEntry(e.id, e.name, () => that.setState(() {
              nutritionsResponse = NutritionService.fetchNutritions();
            }));
            //     padding: EdgeInsets.all(4),
            //     child: ElevatedButton(child: Text(e.name), onPressed: () {}, onHover: (s) {
            //       debugPrint(this.toString());
            //     })
            // );this
            // return Row(children: [the_button], mainAxisAlignment: MainAxisAlignment.center,);
            return the_button;
          }).toList();

          return Column(mainAxisAlignment: MainAxisAlignment.center, children:
          [
            Row(children: buttons, mainAxisAlignment: MainAxisAlignment.center,),
            const SizedBox(height: 10,),
            ElevatedButton(child: Text('+'), onPressed: () {
              showDialog(
                  context: context,
                  builder: (context) {
                    return AlertDialog(
                      title: Text('New nutrition name'),
                      content: TextField(controller: textController),
                      actions: <Widget>[
                        MaterialButton(
                          color: Colors.green,
                          textColor: Colors.white,
                          child: const Text('OK'),
                          onPressed: () {
                            NutritionService.addNutrition(textController.text).whenComplete(() => that.setState(() {
                              nutritionsResponse = NutritionService.fetchNutritions();
                            }));
                            Navigator.pop(context);
                          }
                        )
                      ]
                    );
                  }
              );
            })
          ]);
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

Future<void> main() async {
  final rootNagivatorKey = GlobalKey<NavigatorState>();
  final shellNavigatorKey = GlobalKey<NavigatorState>();

  final router = GoRouter(
    navigatorKey: rootNagivatorKey,
    initialLocation: '/',
    routes: <RouteBase>[
      GoRoute(
          name: 'main',
          path: '/',
          builder: (context, state) {
            return DefaultTabController(
                length: 2,
                child: Scaffold(
                    appBar: AppBar(
                        bottom: TabBar(tabs: [
                          Tab(icon: Icon(Icons.abc)),
                          Tab(icon: Icon(Icons.ac_unit))
                        ]),
                        title: Text('Calories')
                    ),
                    body: TabBarView(children: [
                      MyScaffold(),
                      Products(),
                    ])
                )
            );
          }
      ),
      GoRoute(
          name: 'composeProduct',
          path: '/composeProduct',
          builder: (context, state) {
            return Scaffold(body: ComposeProduct());
          })
      // ShellRoute(
      //   navigatorKey: shellNavigatorKey,
      //   builder: (context, state, child) {
      //
      //   },
      //   routes: <RouteBase>[
      //     GoRoute(
      //         path: '/',
      //         builder: (context, state) {
      //
      //         })
      //   ]
      // )
    ]
  );
  runApp(
    MaterialApp.router(
      routerConfig: router,
      title: 'My app', // used by the OS task switcher
    ));
}