import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../styles/colors.dart';
import '../widgets/note_title.dart';

class CreateNote extends StatefulWidget {
  _CreateNote createState() => _CreateNote();
}

class _CreateNote extends State<CreateNote> {
  String noteTitle = '';
  String noteText = '';

  final TextEditingController _titleTextController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Create Note',
      home: Scaffold(
        backgroundColor: secondaryBg,
        appBar: AppBar(
          automaticallyImplyLeading: false,
          backgroundColor: secondaryBg,
          elevation: 0,
          title: NoteTitle(_titleTextController),
          systemOverlayStyle: SystemUiOverlayStyle.light,
          actions: <Widget>[
            IconButton(
              icon: const Icon(Icons.close),
              color: primaryText,
              tooltip: 'Close',
              onPressed: () => {
                Navigator.of(context).pop()
              },
            ),
          ],
        ),
      ),
    );
  }
}