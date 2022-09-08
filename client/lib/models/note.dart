class Note {
  int? id;
  String title;
  String text;

  Note({
    this.id = null,
    this.title = "No title",
    this.text = "No text"
});

  Map<String, dynamic> toMap() {
    Map<String, dynamic> data = Map<String, dynamic>();
    if (id != null) {
      data['id'] = id;
    }
    data['title'] = title;
    data['text'] = text;
    return data;
  }

  @override toString() {
    return {
      'id': id,
      'title': title,
      'text': text
    }.toString();
  }
}