import 'dart:io';
import 'dart:typed_data';

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
  final args;

  const CreateNote(this.args);
  _CreateNote createState() => _CreateNote();
}

class _CreateNote extends State<CreateNote> {
  String noteTitle = '';
  String noteText = '';
  ui.Image? image;
  String? image_path = '';

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
    noteTitle = (widget.args[0] == 'new' ? '' : widget.args[1]['title']);
    noteText = (widget.args[0] == 'new' ? '' : widget.args[1]['text']);

    _titleTextController.text =
        (widget.args[0] == 'new' ? '' : widget.args[1]['title']);
    _textController.text =
        (widget.args[0] == 'new' ? '' : widget.args[1]['text']);

    _getImage(widget.args[1]['image']);

    _titleTextController.addListener(handleTitleTextChange);
    _textController.addListener(handleTextChange);
  }

  _getFromGallery() async {
    final ImagePicker picker = ImagePicker();
    final XFile? imageFile =
        await picker.pickImage(source: ImageSource.gallery);
    if (imageFile != null) {
      image_path = imageFile.path;
      Uint8List bytes;
      bytes = await File(imageFile.path!).readAsBytes();
      ui.Codec codec = await ui.instantiateImageCodec(bytes);
      ui.FrameInfo frame = await codec.getNextFrame();
      image = frame.image;
      setState(() {});
    }
  }

  Future<void> _getImage(path) async {
    Uint8List bytes;
    bytes = await File(path).readAsBytes();
    ui.Codec codec = await ui.instantiateImageCodec(bytes);
    ui.FrameInfo frame = await codec.getNextFrame();
    image = frame.image;
    setState(() {});
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

  Future<void> _updateNote(Note note) async {
    NotesDatabase notesDb = NotesDatabase();
    await notesDb.initDatabase();
    int result = await notesDb.updateNote(note);
    await notesDb.closeDatabase();
  }

  void handleSaveBtn() async {
    if (noteTitle.length == 0) {
      if (noteText.length == 0) {
        Navigator.pop(context);
        return;
      } else {
        String title = noteText.split('\n')[0];
        if (title.length > 31) {
          title = title.substring(0, 31);
        }
        setState(() {
          noteTitle = title;
        });
      }
    }

    if (widget.args[0] == 'new') {
      Note noteObj = Note(title: noteTitle, text: noteText, image: image_path);
      try {
        await _insertNote(noteObj);
      } catch (e) {
      } finally {
        Navigator.pop(context);
        return;
      }
    }

    // Update Note
    else if (widget.args[0] == 'update') {
      Note noteObj =
          Note(id: widget.args[1]['id'], title: noteTitle, text: noteText, image: image_path);
      try {
        await _updateNote(noteObj);
      } catch (e) {
      } finally {
        Navigator.pop(context);
        return;
      }
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
                    size: Size(MediaQuery.of(context).size.width * 0.96,
                        MediaQuery.of(context).size.height * 0.5),
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
