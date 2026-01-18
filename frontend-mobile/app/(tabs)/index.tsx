import { useState } from 'react';
import { StyleSheet, TextInput, TouchableOpacity, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';
import { chatAPI, Message } from '@/services/api';

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);
    setInput('');

    try {
      const response = await chatAPI.sendMessage({
        message: input,
        conversation_id: 'mobile-session-123'
      });

      const aiMsg: Message = { 
        role: 'assistant', 
        content: response.response 
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error('Error:', error);
      // Adiciona mensagem de erro
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Erro ao comunicar com o servidor. Tenta novamente.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={100}
    >
      <ThemedView style={styles.header}>
        <ThemedText type="title">🪙 Crypto Intelligence</ThemedText>
      </ThemedView>

      <ScrollView style={styles.messagesContainer}>
        {messages.map((msg, i) => (
          <ThemedView 
            key={i} 
            style={[
              styles.messageBubble,
              msg.role === 'user' ? styles.userBubble : styles.aiBubble
            ]}
          >
            <ThemedText style={msg.role === 'user' ? styles.userText : styles.aiText}>
              {msg.content}
            </ThemedText>
          </ThemedView>
        ))}
        {loading && (
          <ThemedView style={styles.loadingBubble}>
            <ThemedText>A pensar...</ThemedText>
          </ThemedView>
        )}
      </ScrollView>

      <ThemedView style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Pergunta sobre crypto..."
          placeholderTextColor="#999"
          onSubmitEditing={sendMessage}
          editable={!loading}
        />
        <TouchableOpacity 
          style={styles.sendButton}
          onPress={sendMessage}
          disabled={loading || !input.trim()}
        >
          <ThemedText style={styles.sendButtonText}>Enviar</ThemedText>
        </TouchableOpacity>
      </ThemedView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  messagesContainer: {
    flex: 1,
    padding: 16,
  },
  messageBubble: {
    padding: 12,
    borderRadius: 16,
    marginBottom: 8,
    maxWidth: '80%',
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#007AFF',
  },
  aiBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#E5E5EA',
  },
  userText: {
    color: '#fff',
  },
  aiText: {
    color: '#000',
  },
  loadingBubble: {
    alignSelf: 'flex-start',
    padding: 12,
    borderRadius: 16,
    backgroundColor: '#E5E5EA',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    gap: 8,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    fontSize: 16,
  },
  sendButton: {
    backgroundColor: '#007AFF',
    borderRadius: 20,
    paddingHorizontal: 20,
    justifyContent: 'center',
  },
  sendButtonText: {
    color: '#fff',
    fontWeight: '600',
  },
});