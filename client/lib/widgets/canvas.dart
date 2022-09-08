import 'package:client/styles/colors.dart';
import 'package:flutter/material.dart';

class ImageCanvas extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = primaryBg;
    canvas.drawPaint(paint);

    final icon = Icons.photo_size_select_actual;
    TextPainter textPainter = TextPainter(textDirection: TextDirection.rtl);
    textPainter.text = TextSpan(
        text: String.fromCharCode(icon.codePoint),
        style: TextStyle(fontSize: 150.0, fontFamily: icon.fontFamily, color: primaryIcon));
    textPainter.layout();
    textPainter.paint(canvas, Offset(size.width / 2 - textPainter.width / 2, size.height / 2 - textPainter.height / 2));
  }

  @override
  bool shouldRepaint(CustomPainter old) {
    return false;
  }
}
