import 'package:flutter/material.dart';

import '../styles/colors.dart';

class NoteText extends StatelessWidget {
  final _textFieldController;

  NoteText(this._textFieldController);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsetsDirectional.fromSTEB(0, 8, 0, 0),
      child: TextField(
        obscureText: false,
        controller: _textFieldController,
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
    );
  }
}