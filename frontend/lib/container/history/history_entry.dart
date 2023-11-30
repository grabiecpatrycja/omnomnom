import 'package:equatable/equatable.dart';

class HistoryEntryModel extends Equatable {
  final num mass;
  final DateTime date;

  const HistoryEntryModel({required this.mass, required this.date});

  static HistoryEntryModel fromMap(Map map) {
    return HistoryEntryModel(
      mass: map['mass'],
      date: map['date'],
    );
  }

  @override
  List<Object> get props => [mass, date];
}