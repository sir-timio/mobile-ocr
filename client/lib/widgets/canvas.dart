import 'dart:ui';

import 'package:client/styles/colors.dart';
import 'package:flutter/material.dart';
import 'dart:ui' as ui;

class ImageCanvas extends CustomPainter {
  ImageCanvas({required this.image, this.points});

  ui.Image? image;
  List<dynamic>? points;

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = primaryBg;
    canvas.drawPaint(paint);

    if (image != null) {
      paintImage(
          canvas: canvas,
          rect: Rect.fromLTRB(0, 0, size.width, size.height),
          image: image!,
          fit: BoxFit.scaleDown
      );

      Size inputSize = Size(image!.width.toDouble(), image!.height.toDouble());
      Size outputSize = Size(size.width.toDouble(), size.height.toDouble());

      Size destinationSize;
      destinationSize = inputSize;
      final double aspectRatio = inputSize.width / inputSize.height;
      if (destinationSize.height > outputSize.height) {
        destinationSize = Size(outputSize.height * aspectRatio, outputSize.height);
      }
      if (destinationSize.width > outputSize.width) {
        destinationSize = Size(outputSize.width, outputSize.width / aspectRatio);
      }

      var scaleX = destinationSize.width / inputSize.width;
      var scaleY = destinationSize.height / inputSize.height;

      var offsetX = (outputSize.width - destinationSize.width) / 2;
      var offsetY = (outputSize.height - destinationSize.height) / 2;

      var framePaint = Paint()
        ..color = secondary
        ..strokeWidth = 1;

      if (points!.length > 0) {
        for (var i = 0; i < points!.length; i++) {
          var leftUp = Offset(points![i][0][0] * scaleX + offsetX, points![i][1][0] * scaleY + offsetY);
          var leftDown = Offset(points![i][0][0] * scaleX + offsetX, points![i][1][1] * scaleY + offsetY);
          var RightUp = Offset(points![i][0][1] * scaleX + offsetX, points![i][1][0] * scaleY + offsetY);
          var downRight = Offset(points![i][0][1] * scaleX + offsetX, points![i][1][1] * scaleY + offsetY);

          //print(leftUp);
          //print(downRight);
          //print('--');
          canvas.drawLine(leftUp, leftDown, framePaint);
          canvas.drawLine(leftDown, downRight, framePaint);
          canvas.drawLine(downRight, RightUp, framePaint);
          canvas.drawLine(leftUp, RightUp, framePaint);
        }
      }
    } else {
      const icon = Icons.photo_size_select_actual;
      TextPainter textPainter = TextPainter(textDirection: TextDirection.rtl);
      textPainter.text = TextSpan(
          text: String.fromCharCode(icon.codePoint),
          style: TextStyle(
              fontSize: 150.0,
              fontFamily: icon.fontFamily,
              color: primaryIcon));
      textPainter.layout();
      textPainter.paint(
          canvas,
          Offset(size.width / 2 - textPainter.width / 2,
              size.height / 2 - textPainter.height / 2));
    }
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) {
    return false;
  }
}
