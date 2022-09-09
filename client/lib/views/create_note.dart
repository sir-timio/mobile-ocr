import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../styles/colors.dart';
import '../widgets/canvas.dart';
import '../widgets/note_title.dart';
import 'dart:ui' as ui;

class CreateNote extends StatefulWidget {
  _CreateNote createState() => _CreateNote();
}

class _CreateNote extends State<CreateNote> {
  String noteTitle = '';
  String noteText = '';
  ui.Image? image;

  final TextEditingController _titleTextController = TextEditingController();

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
                    size: Size(MediaQuery.of(context).size.width * 0.96, 450),
                    painter: ImageCanvas(image: image),
                  ),
                ),
              ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsetsDirectional.fromSTEB(0, 8, 0, 0),
                  child: TextFormField(
                    obscureText: false,
                    decoration: InputDecoration(
                      hintText: 'Enter text...',
                      enabledBorder: OutlineInputBorder(
                        borderSide: BorderSide(
                          color: primaryBg,
                          width: 2,
                        ),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderSide: BorderSide(
                          color: primaryBg,
                          width: 2,
                        ),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      fillColor: secondaryBg,
                      contentPadding:
                          const EdgeInsetsDirectional.fromSTEB(20, 32, 20, 12),
                    ),
                    textAlign: TextAlign.start,
                    maxLines: 100,
                  ),
                ),
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
                            print('Button pressed ...');
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
