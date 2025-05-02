import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatbotAPI {
  final String baseUrl;

  ChatbotAPI(
      {this.baseUrl = 'http://192.168.1.43:5000/chat'}); // Flask api adresi

  Future<String> sendMessage(String message) async {
    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'message': message}),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['response']; // Bot cevabı
    } else {
      throw Exception('Failed to get response from bot');
    }
  }
}
