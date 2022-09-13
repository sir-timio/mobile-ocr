import 'package:flutter/material.dart';

import '../styles/colors.dart';

class Note extends StatelessWidget {
  final notesData;
  final selectedNoteIds;
  final selectedNote;
  final callAfterNavigatorPop;
  final handleNoteListLongPress;
  final handleNoteListTapAfterSelect;

  Note(
      this.notesData,
      this.selectedNoteIds,
      this.selectedNote,
      this.callAfterNavigatorPop,
      this.handleNoteListLongPress,
      this.handleNoteListTapAfterSelect,
      );

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 2.0),
      child: Material(
        elevation: 1,
        color: (selectedNote == false ? secondaryBg : primaryAccent),
        clipBehavior: Clip.hardEdge,
        borderRadius: BorderRadius.circular(5.0),
        child: InkWell(
          onTap: () {
            if (selectedNote == false) {
              if (selectedNoteIds.length == 0) {
              } else {
                handleNoteListLongPress(notesData['id']);
              }
            } else {
              handleNoteListTapAfterSelect(notesData['id']);
            }
          },
          onLongPress: () {
            handleNoteListLongPress(notesData['id']);
          },
          child: Container(
            width: MediaQuery.of(context).size.width,
            padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 8.0),
            child: Row(
              children: <Widget>[
                Expanded(
                  flex: 5,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      Text(
                        notesData['title'] != null ? notesData['title'] : "",
                        style: TextStyle(
                          color: primaryText,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Container(
                        height: 3,
                      ),
                      Text(
                        notesData['text'] != null
                            ? notesData['text'].length > 32
                            ? notesData['text'].substring(0, 32) + "..."
                            : notesData['text'].split('\n')[0]
                            : "",
                        style: TextStyle(
                          color: secondaryText,
                          fontSize: 16,
                          fontWeight: FontWeight.w300,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}