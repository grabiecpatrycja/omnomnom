import 'dart:convert';

import 'package:calcounter/nutrition.dart';

import 'conf.dart' as conf;
import 'package:http/http.dart' as http;

class NutritionService {
  const NutritionService();

  static Future<http.Response> addNutrition(String name) async {
    Uri url = Uri.parse("${conf.BACKEND_URL}/api/nutritions/");
    return await http.post(url, body: {'name': name});
  }

  static Future<http.Response> deleteNutrition(int id) async {
    Uri url = Uri.parse("${conf.BACKEND_URL}/api/nutritions/${id}/");
    return await http.delete(url);
  }

  static Future<List<Nutrition>> fetchNutritions() async {
    final response = await http.get(Uri.parse('http://localhost:8000/api/nutritions'));
    final data = jsonDecode(response.body);
    List<Nutrition> nutritions = [];

    for (final entry in data) {
      nutritions.add(Nutrition(name: entry['name'], id: entry['id']));
    }
    return nutritions;
  }
}