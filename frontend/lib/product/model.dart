import 'package:flutter/material.dart';

class Product {
  final String name;
  final int id;
  Map<String, Object>? nutrients;

  Product({
    required this.id,
    required this.name,
    this.nutrients,
  });

  Product.fromMap(Map map) : name = map['name'], id = map['id'] {
    if (map.containsKey('nutrition_entries')) {
      List data = map['nutrition_entries'] as List;
      Map<String, Object> nutrients = {};
      for (final e in data) {
        Map entry = e as Map;
        nutrients[entry['nutrition_name'] as String] = entry['value'];
      }

      this.nutrients = nutrients;
    }
  }


}