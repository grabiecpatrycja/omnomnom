import 'package:calcounter/container/history/history_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'history_entry.dart';


class ContainerHistory extends StatelessWidget {
  Widget onSuccess(HistoryState state, context) {
        return Table(
            defaultColumnWidth: const FixedColumnWidth(20),
            children: state.entries.map((HistoryEntryModel entry) {
              return TableRow(
                  children: [
                    Container(
                      margin: EdgeInsets.all(10),
                      width: 50,
                      child: Text("${entry.date.year}-${entry.date.month}-${entry.date.day}, ${entry.date.hour}:${entry.date.minute}"),
                    ),
                    Container(
                        width: 50,
                        child: Text(entry.mass.toString())
                    )
                  ]
              );
            }).cast<TableRow>().toList()
        );
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<HistoryBloc, HistoryState>(builder: (context, state) {
      switch (state.status) {
        case HistoryStatus.initial:
          return const Text("Loading...");
        case HistoryStatus.success:
          return onSuccess(state, context);
        case HistoryStatus.failure:
          return const Text("wyjebawszy coś");
      }
    });
  }

}

class ContainerHistoryPage extends StatelessWidget {
  final int containerId;

  const ContainerHistoryPage({
    required this.containerId,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => HistoryBloc()..add(FetchHistory(containerId)),
      child: ContainerHistory(),
    );
  }

}