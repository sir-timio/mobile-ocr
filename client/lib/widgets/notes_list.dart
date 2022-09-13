import 'package:flutter/material.dart';
import 'note.dart';

class NotesList extends StatelessWidget {
  final data;
  final selectedNoteIds;
  final afterNavigatorPop;
  final handleNoteListLongPress;
  final handleNoteListTapAfterSelect;

  NotesList(
      this.data,
      this.selectedNoteIds,
      this.afterNavigatorPop,
      this.handleNoteListLongPress,
      this.handleNoteListTapAfterSelect,
      );

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
        itemCount: data.length,
        itemBuilder: (context, index) {
          dynamic item = data[index];
          return Note(
            item,
            selectedNoteIds,
            (selectedNoteIds.contains(item['id']) == false ? false : true),
            afterNavigatorPop,
            handleNoteListLongPress,
            handleNoteListTapAfterSelect,
          );
        });
  }
}