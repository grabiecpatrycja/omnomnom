class OContainer {
  final String name;
  int? id;

  OContainer({required this.name, this.id});
  OContainer.fromMap(Map data) : name = data['name'] {
    if(data.containsKey('id')) {
      id = data['id'];
    }
  }

  Map toMap() {
    return {
      'name': name,
      'id': id,
    };
  }

}