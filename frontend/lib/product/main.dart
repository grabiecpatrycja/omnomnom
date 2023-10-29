import 'dart:convert';

import 'package:calcounter/http/nutrition.dart';
import 'package:calcounter/http/product.dart';
import 'package:calcounter/nutrition.dart';
import 'package:calcounter/product/composeProduct.dart';
import 'package:calcounter/product/model.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart' as http;


class ProductLink extends StatelessWidget {
  final int id;
  final String name;
  const ProductLink({required this.id, required this.name, super.key});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(name),
      onTap: () {
        GoRouter.of(context).push("/products/${id}");
      },
    );
  }
}


class ProductState extends State<Products> {
  late Future<http.Response> productsResponse;
  late Future<List<Nutrition>> nutritionsResponse;
  late Future both;

  @override
  void initState() {
    super.initState();
    productsResponse = ProductService.fetchProducts();
    nutritionsResponse = NutritionService.fetchNutritions();
    both = Future.wait([productsResponse, nutritionsResponse]);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(future: both, builder: (context, snapshot) {
      if (snapshot.connectionState == ConnectionState.done) {
        List<Product> data = (jsonDecode(snapshot.data[0]!.body) as List<
            dynamic>)
            .map((e) => Product(id: e['id'], name: e['name']))
            .toList();

        return Column(children: [
          Expanded(child: ListView.builder(
              scrollDirection: Axis.vertical,
              shrinkWrap: true,
              itemCount: data.length,
              itemBuilder: (context, index) {
                Product product = data[index];
                return ProductLink(id: product.id, name: product.name);
              })),
          MaterialButton(child: const Text('Compose a new product'), onPressed: () {
            GoRouter.of(context).goNamed('composeProduct');
          })
        ],
        );
      }
      return const Text('nie pobrano :/');
    });
  }

}

class Products extends StatefulWidget {

  @override
  State<StatefulWidget> createState() {
    return ProductState();
  }

}