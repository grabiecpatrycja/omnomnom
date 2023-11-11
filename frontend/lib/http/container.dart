import 'dart:convert';

import '../container/models.dart';
import 'package:http/http.dart' as http;
import 'conf.dart' as conf;

class ContainerService {
  static Future<List<OContainer>> fetchContainers() async {
    Uri url = Uri.parse("${conf.BACKEND_URL}/api/containers/");

    http.Response response = await http.get(url);
    List data = jsonDecode(utf8.decode(response.bodyBytes));
    List<Map> casted = data.cast<Map>();
    return casted.map((Map m) => OContainer.fromMap(m)).toList();
  }

  static Future<OContainer> fetchContainer(int id) async {
    Uri url = Uri.parse("${conf.BACKEND_URL}/api/containers/${id}");

    final response = await http.get(url);
    return OContainer.fromMap(jsonDecode(utf8.decode(response.bodyBytes)));
  }
}