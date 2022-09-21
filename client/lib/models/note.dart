import 'dart:typed_data';

class Note {
  int? id;
  String title;
  String text;
  String? image;
  String? points;

  Note({
    this.id = null,
    this.title = "No title",
    this.text = "No text",
    this.image,
    this.points
});

  Map<String, dynamic> toMap() {
    Map<String, dynamic> data = Map<String, dynamic>();
    if (id != null) {
      data['id'] = id;
    }
    data['title'] = title;
    data['text'] = text;
    data['image'] = image;
    data['points'] = points;
    return data;
  }

  @override toString() {
    return {
      'id': id,
      'title': title,
      'text': text,
      'image': image,
      'points': points
    }.toString();
  }
}