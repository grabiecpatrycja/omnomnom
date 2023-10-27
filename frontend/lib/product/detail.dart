import 'dart:collection';
import 'dart:convert';

import 'package:calcounter/http/nutrition.dart';
import 'package:calcounter/nutrition.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:http/http.dart';

import '../http/product.dart';

String findNutrition(List<Nutrition> nutritions, int id) {
  for (final nutrition in nutritions) {
    if (nutrition.id == id){
      return nutrition.name;
    }
  }
  return '';
}



class ProductDetail extends StatelessWidget {
  final int id;
  const ProductDetail({required this.id, super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(future: Future.wait([
      ProductService.fetchProduct(id),
      NutritionService.fetchNutritions(),
    ]),builder: (context, snapshot){
      if (snapshot.hasData) {
        final HashMap<String, dynamic> data = jsonDecode((snapshot.data![0] as Response).body);
        final List<Nutrition> nutritions = snapshot.data![1] as List<Nutrition>;

        (data['nutrition_entries'] as List).map((e) {
          final HashMap nutrition_entry = e as HashMap;
        });
        return Table(
          border: TableBorder.all(),
          columnWidths: const <int, TableColumnWidth>{},
          children: []
        );
      }
      else {
        return const Text('Loading...');
      }
    });
  }
}
