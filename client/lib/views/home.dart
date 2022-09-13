import 'package:client/styles/colors.dart';
import 'package:client/views/create_note.dart';
import 'package:client/widgets/notes_list.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../models/database.dart';

Future<List<Map<String, dynamic>>> readDatabase() async {
  try {
    NotesDatabase notesDb = NotesDatabase();
    await notesDb.initDatabase();
    List<Map> notesList = await notesDb.getAllNotes();
    await notesDb.closeDatabase();
    List<Map<String, dynamic>> notesData =
        List<Map<String, dynamic>>.from(notesList);
    notesData.sort((a, b) => (a['title']).compareTo(b['title']));
    return notesData;
  } catch (e) {
    print('Error retrieving notes');
    return [{}];
  }
}

class Home extends StatefulWidget {
  @override
  _Home createState() => _Home();
}

class _Home extends State<Home> {
  List<Map<String, dynamic>>? notesData;
  List<int> selectedNoteIds = [];

  void afterNavigatorPop() {
    setState(() {});
  }

// Long Press handler to display bottom bar
  void handleNoteListLongPress(int id) {
    setState(() {
      if (selectedNoteIds.contains(id) == false) {
        selectedNoteIds.add(id);
      }
    });
  }

// Remove selection after long press
  void handleNoteListTapAfterSelect(int id) {
    setState(() {
      if (selectedNoteIds.contains(id) == true) {
        selectedNoteIds.remove(id);
      }
    });
  }

  void handleDelete() async {
    try {
      NotesDatabase notesDb = NotesDatabase();
      await notesDb.initDatabase();
      for (int id in selectedNoteIds) {
        int result = await notesDb.deleteNote(id);
      }
      await notesDb.closeDatabase();
    } catch (e) {
      print('Cannot delete notes');
    } finally {
      setState(() {
        selectedNoteIds = [];
      });
    }
  }

  void refreshPage() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Notes',
      home: Scaffold(
        backgroundColor: primaryBg,
        appBar: AppBar(
          automaticallyImplyLeading: false,
          elevation: 2,
          backgroundColor: (selectedNoteIds.length > 0 ? primary : secondaryBg),
          leadingWidth: (selectedNoteIds.length > 0 ? 56 : 0),
          title: Text(
            (selectedNoteIds.length > 0
                ? ('Selected ' +
                    selectedNoteIds.length.toString() +
                    '/' +
                    notesData!.length.toString())
                : 'Notes'),
            style: TextStyle(
              color: (selectedNoteIds.length > 0 ? secondaryBg : primary),
            ),
          ),
          leading: (selectedNoteIds.length > 0
              ? IconButton(
                  onPressed: () {
                    setState(() {
                      selectedNoteIds = [];
                    });
                  },
                  icon: Icon(
                    Icons.close,
                    color: secondaryBg,
                  ),
                )
              : Container()),
          systemOverlayStyle: SystemUiOverlayStyle.light,
          actions: [
            (selectedNoteIds.length > 0
                ? IconButton(
                    icon: Icon(
                      Icons.delete,
                      color: secondaryBg,
                    ),
                    tooltip: 'Delete',
                    onPressed: () => handleDelete(),
                  )
                : Container()),
          ],
        ),
        floatingActionButton: FloatingActionButton(
          tooltip: 'New Note',
          backgroundColor: primary,
          elevation: 2,
          onPressed: () => {
            Navigator.of(context)
                .push(_createRoute())
                .then((res) => refreshPage())
          },
          child: Icon(
            Icons.add,
            color: primaryBg,
          ),
        ),
        body: Padding(
          padding: const EdgeInsetsDirectional.fromSTEB(0, 8, 0, 8),
          child: FutureBuilder(
              future: readDatabase(),
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  notesData = snapshot.data;
                  return Stack(
                    children: <Widget> [
                      // Display Notes
                      NotesList(
                        snapshot.data,
                        this.selectedNoteIds,
                        afterNavigatorPop,
                        handleNoteListLongPress,
                        handleNoteListTapAfterSelect,
                      ),
                    ],
                  );
                } else if (snapshot.hasError) {
                  print('Error reading database');
                  return Text("No widget to build");
                } else {
                  return Center(
                    child: CircularProgressIndicator(
                      backgroundColor: secondaryBg,
                    ),
                  );
                }
              }),
        ),
      ),
    );
  }
}

Route _createRoute() {
  return PageRouteBuilder(
    pageBuilder: (context, animation, secondaryAnimation) => CreateNote(),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      const begin = Offset(0.0, 1.0);
      const end = Offset.zero;
      const curve = Curves.ease;

      var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

      return SlideTransition(
        position: animation.drive(tween),
        child: child,
      );
    },
  );
}
