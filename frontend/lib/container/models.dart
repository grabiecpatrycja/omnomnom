typedef ProductRecord = ({num mass, num id});


class OContainer {
  final String name;
  int? id;
  Map<String, ProductRecord>? products;

  OContainer({required this.name, this.id, this.products});
  OContainer.fromMap(Map data) : name = data['name'] {
    if(data.containsKey('id')) {
      id = data['id'];
    }

    if(data.containsKey('product_entries')) {
      Map<String, ProductRecord> products = {};

      final product_entries = data['product_entries'];
      for(final product_entry in product_entries) {
        products[product_entry['product_name']] = (mass: product_entry['mass'] as num, id: product_entry['product']);
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