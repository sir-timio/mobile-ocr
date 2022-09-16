import 'dart:ffi' as ffi;
import 'dart:io';
import 'dart:typed_data';

import 'package:client/widgets/note_text.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path_provider/path_provider.dart';

import '../styles/colors.dart';
import '../widgets/canvas.dart';
import '../widgets/note_title.dart';
import 'dart:ui' as ui;
import '../models/note.dart';
import '../models/database.dart';
import 'package:http/http.dart' as http;
import 'dart:convert' as convert;
import 'package:path/path.dart' as path;

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
  List<dynamic>? points = [];

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

  Future<void> _showAlert(String text) async {
    return showDialog<void>(
      context: context,
      barrierDismissible: false, // user must tap button!
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Error!'),
          content: SingleChildScrollView(
            child: ListBody(
              children: <Widget>[
                Text(text),
              ],
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Close'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
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
    points = (widget.args[1]['points'] != null ? _getPoints(widget.args[1]['points']) : []);

    _titleTextController.addListener(handleTitleTextChange);
    _textController.addListener(handleTextChange);
  }

  _getFromGallery() async {
    final ImagePicker picker = ImagePicker();
    final XFile? imageFile =
        await picker.pickImage(source: ImageSource.gallery);
    if (imageFile != null) {
      Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
      String appDocumentsPath = appDocumentsDirectory.path;
      var fileName = path.basename(imageFile.path!);
      await imageFile.saveTo('$appDocumentsPath/$fileName');
      image_path = '$appDocumentsPath/$fileName';
      Uint8List bytes;
      bytes = await File(image_path!).readAsBytes();
      ui.Codec codec = await ui.instantiateImageCodec(bytes);
      ui.FrameInfo frame = await codec.getNextFrame();
      image = frame.image;
      points = [];
      setState(() {});
    }
  }

  List<dynamic> _getPoints(points) {
    List<dynamic> result = convert.jsonDecode(points);
    List<dynamic> p = [];
    for (var i = result.length - 1; i >= 0; i--) {
      p!.add([result[i][0], result[i][1]]);
    }
    return p;
  }

  Future<void> _getImage(path) async {
    Uint8List bytes;
    bytes = await File(path).readAsBytes();
    image_path = path;
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
        _showAlert('Note is empty!');
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

    String strPoints = '[]';
    if (points!.length > 0) {
      strPoints = '[';
      for (var i = 0; i < points!.length - 1; i++) {
        strPoints += '[' +
            points![i][0].toString() +
            ', ' +
            points![i][1].toString() +
            '], ';
      }
      strPoints += '[' +
          points![points!.length - 1][0].toString() +
          ',' +
          points![points!.length - 1][1].toString() +
          ']';
      strPoints += ']';
    }

    if (widget.args[0] == 'new') {
      Note noteObj = Note(
          title: noteTitle,
          text: noteText,
          image: image_path,
          points: strPoints);
      try {
        await _insertNote(noteObj);
      } catch (e) {
        _showAlert(e.toString());
        return;
      } finally {
        Navigator.pop(context);
        return;
      }
    } else if (widget.args[0] == 'update') {
      Note noteObj = Note(
          id: widget.args[1]['id'],
          title: noteTitle,
          text: noteText,
          image: image_path,
          points: strPoints);
      try {
        await _updateNote(noteObj);
      } catch (e) {
        _showAlert(e.toString());
        return;
      } finally {
        Navigator.pop(context);
        return;
      }
    }
  }

  Future<String> upload(filepath) async {
    try {
      Uint8List bytes = File(filepath).readAsBytesSync() as Uint8List;
      final response = await http.post(
        Uri.parse("http://127.0.0.1:8080/predict"),
        body: bytes,
      );
      List<dynamic> result = convert.jsonDecode(response.body);
      noteText = '';
      points = [];
      for (var i = result.length - 1; i >= 0; i--) {
        points!.add(result[i][0]);
        if (result[i][1] == '') {
          noteText += ' ';
        } else {
          noteText += result[i][1] + ' ';
        }
      }
      _textController.text = noteText;
      setState(() {});
    } catch (e) {
      _showAlert(e.toString());
      print(e);
    }
    return '';
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
        body: SingleChildScrollView(
          physics: ClampingScrollPhysics(),
          child: Padding(
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
                      painter: ImageCanvas(image: image, points: points),
                    ),
                  ),
                ),
                Container(
                  height: MediaQuery.of(context).size.height * 0.5 - 210,
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
                              print('Recognize button pressed ...');
                              upload(image_path!);
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
      ),
    );
  }
}
