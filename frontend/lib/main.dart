import 'dart:convert';

import 'package:calcounter/container/detail.dart';
import 'package:calcounter/container/history/widgets.dart';
import 'package:calcounter/container/main.dart';
import 'package:calcounter/entry.dart';
import 'package:calcounter/http/nutrition.dart';
import 'package:calcounter/product/composeProduct.dart';
import 'package:calcounter/product/detail.dart';
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
  final productsNavigatorKey = GlobalKey<NavigatorState>();
  final containersNavigatorKey = GlobalKey<NavigatorState>();

  final router = GoRouter(
    navigatorKey: rootNagivatorKey,
    initialLocation: '/',
    routes: <RouteBase>[
      StatefulShellRoute.indexedStack(builder: (context, state, shell) {
        return CustomNavigation(shell: shell);
      }, branches: <StatefulShellBranch>[
        StatefulShellBranch(routes: <RouteBase>[
          GoRoute(
            path: '/',
            builder: (context, state) {
              return NutritionsWidget();
            }
          ),
        ]),
        StatefulShellBranch(
            navigatorKey: productsNavigatorKey,
            routes: <RouteBase>[
          GoRoute(
              path: '/products',
              builder: (context, state) {
                return Products();
              },
              routes: <RouteBase>[
                GoRoute(
                    name: 'composeProduct',
                    path: 'compose',
                    builder: (context, state) {
                      return ComposeProduct();
                    }
                ),
                GoRoute(
                  name: 'productDetails',
                  path: ':productId',
                  builder: (context, state) {
                    return ProductDetail(id: int.parse(state.pathParameters['productId']!));
                  }
                )
              ]
          ),
        ]),
        StatefulShellBranch(
            navigatorKey: containersNavigatorKey,
            routes: <RouteBase>[
          GoRoute(
              path: '/containers',
              builder: (context, state) {
                return OContainers();
              },
              routes: <RouteBase>[
                GoRoute(
                    name: 'containerDetail',
                    path: ':containerId',
                    builder: (context, state) {
                      return ContainerDetailWidget(id: int.parse(state.pathParameters['containerId']!));
                    }
                ),
                GoRoute(
                  name: 'containerHistory',
                  path: ':containerId/history',
                  builder: (context, state) {
                    return ContainerHistoryPage(containerId: int.parse(state.pathParameters['containerId']!));
                  }
                )
              ]
          )
        ]),
      ]),
    ]
  );
  runApp(
    MaterialApp.router(
      routerConfig: router,
      title: 'My app', // used by the OS task switcher
    ));
}


class CustomNavigation extends StatelessWidget {
  const CustomNavigation({
    required StatefulNavigationShell this.shell,
    super.key
  });

  final StatefulNavigationShell shell;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: shell,
      appBar: AppBar(),
      bottomNavigationBar: NavigationBar(
        onDestinationSelected: (index) {
          shell.goBranch(index, initialLocation: index == shell.currentIndex);
        },
        indicatorColor: Colors.amber[800],
        selectedIndex: shell.currentIndex,
        destinations: const <Widget>[
          NavigationDestination(
            selectedIcon: Icon(Icons.home),
            icon: Icon(Icons.home_outlined),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.business),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.abc),
            label: 'Home',
          ),
        ]
      ),
    );
  }
  
}