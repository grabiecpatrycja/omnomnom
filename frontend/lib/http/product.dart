import 'dart:collection';
import 'dart:convert';

import 'package:http/http.dart' as http;
import 'conf.dart' as conf;

class ProductService {
  static Future<http.Response> fetchProducts() async {
    Uri uri = Uri.parse("${conf.BACKEND_URL}/api/products/");
    return await http.get(uri);
  }

  static Future<http.Response> fetchProduct(int id) async {
    Uri uri = Uri.parse("${conf.BACKEND_URL}/api/products/${id}");
    return await http.get(uri);
  }

  static Future<http.Response> addProduct(String name) async {
    Uri uri = Uri.parse("${conf.BACKEND_URL}/api/products/");
    return await http.post(uri, body: {'name': name});
  }

  static Future<http.Response> addNutritionsToProduct(int productId, HashMap<int, double> values) async {
    Uri uri = Uri.parse("${conf.BACKEND_URL}/api/products/${productId}/");
    List<Map<String, num>> payload = values.entries.map((MapEntry<int, double> e) {
      return {
        'nutrition': e.key,
        'value': e.value,
      };

    }).toList();

    return await http.post(uri, body: json.encode(payload));
  }
}