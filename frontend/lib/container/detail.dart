import 'dart:async';
import 'dart:convert';

import 'package:calcounter/container/models.dart';
import 'package:calcounter/http/container.dart';
import 'package:calcounter/product/model.dart';
import 'package:dropdown_search/dropdown_search.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../http/product.dart';


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
  late Future<List<Product>> productResponse;
  late Future<({
    List<Product> products,
    OContainer container,
  })> productsContainer;

  bool showFillRow = false;
  Product? selectedProduct;
  TextEditingController massController = TextEditingController();

  ContainerInsidesState({required this.id});

  @override
  void initState() {
    super.initState();
    containerResponse = ContainerService.fetchContainer(id);
    productResponse = getProducts();
    productsContainer = waitForBoth();
  }

  Future<({List<Product> products, OContainer container})> waitForBoth() {
    return Future.wait([productResponse, containerResponse]).then((response) {
      return (products: response[0] as List<Product>, container: response[1] as OContainer);
    });
  }

  Future<List<Product>> getProducts() async {
    final response = await ProductService.fetchProducts();
    List data = jsonDecode(utf8.decode(response.bodyBytes));
    List<Map> dataMap = data.cast<Map>();
    List<Product> products = dataMap.map((e) => Product.fromMap(e)).toList();
    return products;
  }

  void submitNewProduct() async {
    final container = await containerResponse;
    List<Map<String, num?>> newProducts = [];
    for (final product in container.products!.entries) {
      newProducts.add({
        'product': product.value.id,
        'mass': product.value.mass,
      });
    }

    newProducts.add({
      'product': selectedProduct?.id,
      'mass': num.parse(massController.text),
    });

    ContainerService.putProducts(id, newProducts).then((response) {
      setState(() {
        containerResponse = ContainerService.fetchContainer(id);
        productResponse = getProducts();
        productsContainer = waitForBoth();
        showFillRow = false;
      });
    });
  }

  Future deleteProduct(int productId) async {
    final container = await containerResponse;
    List<Map<String, num?>> newProducts = [];
    for (final product in container.products!.entries) {
      if (product.value.id == productId) {
        continue;
      }

      newProducts.add({
        'product': product.value.id,
        'mass': product.value.mass,
      });
    }

    ContainerService.putProducts(id, newProducts).then((response) {
      setState(() {
        containerResponse = ContainerService.fetchContainer(id);
        productResponse = getProducts();
        productsContainer = waitForBoth();
        showFillRow = false;
      });
    });
  }

  TableRow getFillRow(List<Product> snapshot) {
    return TableRow(children: [
      DropdownSearch<Product>(
        items: snapshot
            .map<Product>((Product product) => product)
            .toList(),
        itemAsString: (Product p) => p.name,
        onChanged: (Product? p) {
          setState(() {
            selectedProduct = p;
          });
        },
      ),
      TextField(
        controller: massController,
        decoration: const InputDecoration(
          border: OutlineInputBorder(),
          hintText: 'Enter the mass',
        ),
      ),
      Center(child: Row(children: [
        IconButton(
          icon: Icon(Icons.check),
          onPressed: () {
            submitNewProduct();
          },
        ),
        IconButton(
          icon: Icon(Icons.close),
          onPressed: () {
            setState(() {
              showFillRow = false;
            });
          },
        )
      ])),
    ]);
  }

  Widget build(BuildContext context) {
    return FutureBuilder(
        future: productsContainer, builder: (context, snapshot) {
      if (!snapshot.hasData) {
        return const Text('Loading...');
      }

      final data = snapshot.data!;
      return Column(children: [
        Table(
          columnWidths: const <int, TableColumnWidth>{
            0: IntrinsicColumnWidth(),
            1: IntrinsicColumnWidth(),
            2: FixedColumnWidth(100),
          },
          children: data.container.products!.entries.map<TableRow>((product_entry) {
            return TableRow(children: [
              Container(
                padding: const EdgeInsets.all(10.0),
                child: Text(product_entry.key as String),
              ),
              Container(
                padding: EdgeInsets.all(10.0),
                child: Text(product_entry.value.mass.toString()),
              ),
              Container(
                padding: EdgeInsets.all(10.0),
                child: IconButton(
                  onPressed: () async {
                    await deleteProduct(product_entry.value.id as int);
                  },
                  icon: const Center(child: Icon(Icons.delete)),
                )
              ),
            ]);
          }).toList() +
              (showFillRow ? <TableRow>[getFillRow(data.products)] : <TableRow>[]),
        ),
        Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              MaterialButton(onPressed: () {
                setState(() {
                  showFillRow = !showFillRow;
                });
              }, child: const Text('Add new entry')),
              MaterialButton(
                onPressed: () {},
                child: const Text('Edit'),
              ),
              IconButton(onPressed: (){
                GoRouter.of(context).goNamed('containerHistory', pathParameters: {'containerId': id.toString()});
              }, icon: Icon(Icons.area_chart))
            ])
      ]);
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