import 'package:calcounter/nutrition.dart';
import 'package:flutter/material.dart';

import '../http/product.dart';
import 'model.dart';

String findNutrition(List<Nutrition> nutritions, int id) {
  for (final nutrition in nutritions) {
    if (nutrition.id == id){
      return nutrition.name;
    }
  }
  return '';
}

class ProductDetail extends StatefulWidget {
  final int id;
  const ProductDetail({required this.id, super.key});

  @override
  State<StatefulWidget> createState() {
    return ProductDetailState(id: id);
  }
}


class ProductDetailState extends State<ProductDetail> {
  final int id;
  late Future<Product> fetchProduct;
  ProductDetailState({required this.id}) : fetchProduct = ProductService.fetchProduct(id);

  @override
  void initState() {
    super.initState();
    fetchProduct = ProductService.fetchProduct(id);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(future: fetchProduct,builder: (context, snapshot){
      if (snapshot.hasData) {
        final product = snapshot.data!;
        return DataTable(columns: const <DataColumn>[
          DataColumn(label: Expanded(child: Text('Name'))),
          DataColumn(label: Expanded(child: Text('Value'))),
        ], rows: product.nutrients!.entries.map((e) {
          return DataRow(cells: <DataCell>[
            DataCell(Text(e.key)),
            DataCell(Text(e.value.toString())),
          ]);
        }).toList());
      }

      return const Text('Nie pobrano');

    });
  }
}
