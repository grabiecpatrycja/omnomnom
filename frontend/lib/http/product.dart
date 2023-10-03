import 'package:http/http.dart' as http;
import 'conf.dart' as conf;

class ProductService {
  static Future<http.Response> fetchProducts() async {
    Uri uri = Uri.parse("${conf.BACKEND_URL}/api/products/");
    return await http.get(uri);
  }
}