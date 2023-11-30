import 'dart:convert';

import 'package:bloc/bloc.dart';
import 'package:calcounter/container/history/history_entry.dart';
import 'package:calcounter/http/container.dart';
import 'package:equatable/equatable.dart';
import 'package:http/http.dart' as http;

enum HistoryStatus {
  initial, success, failure
}

sealed class HistoryEvent{
  const HistoryEvent();
}

final class FetchHistory extends HistoryEvent {
  final int containerId;
  const FetchHistory(this.containerId);

}


final class HistoryState extends Equatable {
  final HistoryStatus status;
  final List<HistoryEntryModel> entries;

  const HistoryState({
    this.status = HistoryStatus.initial,
    this.entries = const [],
  });

  @override
  List<Object> get props => [];

}


class HistoryBloc extends Bloc<HistoryEvent, HistoryState> {
  HistoryBloc(): super(const HistoryState()) {
    on<FetchHistory>(_onFetchHistory);
  }

  Future<void> _onFetchHistory(
      FetchHistory event,
      Emitter<HistoryState> emit)
  async {
    final response = await ContainerService.fetchMassRecords(event.containerId);
    final List data = jsonDecode(response.body);
    final List<HistoryEntryModel> entries = data.cast<Map>().map((entry) => HistoryEntryModel(
        mass: entry['mass'],
        date: DateTime.parse(entry['date']))
    ).toList();

    emit(HistoryState(status: HistoryStatus.success, entries: entries));
  }

}