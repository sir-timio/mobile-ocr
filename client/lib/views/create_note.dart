import 'dart:io';

import 'package:client/widgets/note_text.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../styles/colors.dart';
import '../widgets/canvas.dart';
import '../widgets/note_title.dart';
import 'dart:ui' as ui;
import '../models/note.dart';
import '../models/database.dart';

class CreateNote extends StatefulWidget {
  _CreateNote createState() => _CreateNote();
}

class _CreateNote extends State<CreateNote> {
  String noteTitle = '';
  String noteText = '';
  ui.Image? image;

  final TextEditingController _titleTextController = TextEditingController();
  final TextEditingController _textController = TextEditingController();

  void handleTitleTextChange() {
    setState(() {
      noteTitle = _titleTextController.text.trim();
    });
  }

  void handleTextChange() {
    setState(() {
      noteText = _textController.text.trim();
    });
  }

  @override
  void initState() {
    super.initState();
    _titleTextController.addListener(handleTitleTextChange);
    _textController.addListener(handleTextChange);
  }

  _getFromGallery() async {
    final ImagePicker picker = ImagePicker();
    final XFile? imageFile = await picker.pickImage(source: ImageSource.gallery);
    if (imageFile != null) {
      final path = imageFile.path;
      Uint8List bytes;
      if (kIsWeb) {
        bytes = await imageFile.readAsBytes();
      } else {
        bytes = await File(path).readAsBytes();
      }
      ui.Codec codec = await ui.instantiateImageCodec(bytes);
      ui.FrameInfo frame = await codec.getNextFrame();
      image = frame.image;
      setState(() {});
    }
  }

  @override
  void dispose() {
    _titleTextController.dispose();
    _textController.dispose();
    super.dispose();
  }

  Future<void> _insertNote(Note note) async {
    NotesDatabase notesDb = NotesDatabase();
    await notesDb.initDatabase();
    int result = await notesDb.insertNote(note);
    await notesDb.closeDatabase();
  }

  void handleSaveBtn() async {
    if (noteTitle.length == 0) {
      if (noteText.length == 0) {
        Navigator.pop(context);
        return;
      }
      else {
        String title = noteText.split('\n')[0];
        if (title.length > 31) {
          title = title.substring(0, 31);
        }
        setState(() {
          noteTitle = title;
        });
      }
    }

    Note noteObj = Note(
        title: noteTitle,
        text: noteText
    );

    try {
      await _insertNote(noteObj);
    } catch (e) {
      print(e);
      print('Error inserting row');
    } finally {
      Navigator.pop(context);
      return;
    }
  }

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
              onPressed: () => {Navigator.of(context).pop()},
            ),
          ],
        ),
        body: Padding(
          padding: const EdgeInsetsDirectional.fromSTEB(12, 0, 12, 0),
          child: Column(
            mainAxisSize: MainAxisSize.max,
            children: [
              Padding(
                padding: const EdgeInsetsDirectional.fromSTEB(0, 4, 0, 0),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: CustomPaint(
                    size: Size(MediaQuery.of(context).size.width * 0.96, MediaQuery.of(context).size.height * 0.5),
                    painter: ImageCanvas(image: image),
                  ),
                ),
              ),
              Expanded(
                child: NoteText(_textController),
              ),
              Padding(
                padding: const EdgeInsetsDirectional.fromSTEB(0, 8, 0, 0),
                child: ElevatedButton(
                  onPressed: () {
                    _getFromGallery();
                  },
                  style: ElevatedButton.styleFrom(
                    minimumSize: const Size(double.infinity, 50),
                    backgroundColor: primary,
                    elevation: 2,
                  ),
                  child: const Text('Upload Image'),
                ),
              ),
              Padding(
                padding: const EdgeInsetsDirectional.fromSTEB(0, 8, 0, 8),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: Padding(
                        padding:
                            const EdgeInsetsDirectional.fromSTEB(0, 0, 4, 0),
                        child: ElevatedButton(
                          onPressed: () {
                            print('Button pressed ...');
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: primary,
                            elevation: 2,
                            minimumSize: const Size(double.infinity, 50),
                          ),
                          child: const Text('Recognize'),
                        ),
                      ),
                    ),
                    Expanded(
                      child: Padding(
                        padding:
                            const EdgeInsetsDirectional.fromSTEB(4, 0, 0, 0),
                        child: ElevatedButton(
                          onPressed: () {
                            print('Save button pressed ...');
                            handleSaveBtn();
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: primary,
                            elevation: 2,
                            minimumSize: const Size(double.infinity, 50),
                          ),
                          child: const Text('Save'),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
