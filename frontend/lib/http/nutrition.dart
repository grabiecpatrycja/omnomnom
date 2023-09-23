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
}