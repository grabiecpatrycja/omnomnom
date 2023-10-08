import 'dart:convert';

import 'package:calcounter/http/nutrition.dart';
import 'package:calcounter/http/product.dart';
import 'package:calcounter/nutrition.dart';
import 'package:calcounter/product/composeProduct.dart';
import 'package:calcounter/product/model.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart' as http;

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
          ListView.builder(shrinkWrap: true,
              itemCount: data.length,
              itemBuilder: (context, index) {
                Product product = data[index];
                return ListTile(title: Text(product.name));
              }),
          MaterialButton(child: const Text('Compose a new product'), onPressed: () {
            context.goNamed('composeProduct');
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