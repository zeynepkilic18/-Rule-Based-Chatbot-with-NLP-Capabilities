import 'package:flutter/material.dart';
import '../widgets/chat_bubble.dart';
import '../services/chatbot_api.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  List<Map<String, dynamic>> messages = [];
  final ChatbotAPI _chatbotAPI =
      ChatbotAPI(baseUrl: 'http://192.168.1.43:5000/chat');

  void scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      messages.add({
        "text": " $text", // Mesajı map içine ekle
        "isUser": true, // Kullanıcı mesajı
      });
    });
    scrollToBottom();

    _controller.clear();

    try {
      final response =
          await _chatbotAPI.sendMessage(text); // Apiyle mesaj gönderimi
      setState(() {
        messages.add({
          "text": " $response", // Bot'un cevabı
          "isUser": false, // Bot mesajı
        });
      });
      scrollToBottom();
    } catch (e) {
      setState(() {
        messages.add({
          "text": "Error: Could not get a response from the bot.",
          "isUser": false,
        });
      });
      scrollToBottom();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Chatbot"),
        backgroundColor: Color.fromARGB(255, 162, 211, 233),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(12),
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final msg = messages[index];
                return ChatBubble(
                  text: msg["text"],
                  isUser: msg["isUser"],
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 12),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText:
                          'Write a message...', //Mesaj girdisinin alınması
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(
                  width: 8,
                ),
                IconButton(onPressed: sendMessage, icon: const Icon(Icons.send))
              ],
            ),
          )
        ],
      ),
    );
  }
}
