import 'package:calcounter/container/history/history_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';


class ContainerHistory extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<HistoryBloc, HistoryState>(builder: (context, state) {
      switch (state.status) {
        case HistoryStatus.initial:
          return const Text("Loading...");
        case HistoryStatus.success:
          return const Text("Załadowano :o");
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