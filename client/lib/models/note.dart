import 'dart:typed_data';

class Note {
  int? id;
  String title;
  String text;
  String? image;

  Note({
    this.id = null,
    this.title = "No title",
    this.text = "No text",
    this.image
});

  Map<String, dynamic> toMap() {
    Map<String, dynamic> data = Map<String, dynamic>();
    if (id != null) {
      data['id'] = id;
    }
    data['title'] = title;
    data['text'] = text;
    data['image'] = image;
    return data;
  }

  @override toString() {
    return {
      'id': id,
      'title': title,
      'text': text,
      'image': image
    }.toString();
  }
}