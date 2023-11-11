class OContainer {
  final String name;
  int? id;
  Map? products;

  OContainer({required this.name, this.id, this.products});
  OContainer.fromMap(Map data) : name = data['name'] {
    if(data.containsKey('id')) {
      id = data['id'];
    }

    if(data.containsKey('product_entries')) {
      Map<String, num> products = {};

      final product_entries = data['product_entries'];
      for(final product_entry in product_entries) {
        products[product_entry['product_name']] = product_entry['mass'] as num;
      }

      this.products = products;
    }
  }

  Map toMap() {
    return {
      'name': name,
      'id': id,
    };
  }

}