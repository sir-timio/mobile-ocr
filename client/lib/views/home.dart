import 'package:client/styles/colors.dart';
import 'package:client/views/create_note.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class Home extends StatefulWidget {
  @override
  _Home createState() => _Home();
}

class _Home extends State<Home> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Notes',
      home: Scaffold(
        backgroundColor: primaryBg,
        appBar: AppBar(
          automaticallyImplyLeading: false,
          elevation: 6,
          backgroundColor: secondaryBg,
          title: Text(
            'Notes',
            style: TextStyle(
              color: primary,
              fontWeight: FontWeight.bold,
            ),
          ),
          systemOverlayStyle: SystemUiOverlayStyle.light,
        ),
        floatingActionButton: FloatingActionButton(
          tooltip: 'New Note',
          backgroundColor: primary,
          elevation: 6,
          onPressed: () => {
            Navigator.of(context).push(_createRoute())
          },
          child: Icon(
            Icons.add,
            color: primaryBg,
          ),
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