// frontend-mobile/services/api.ts
import { Platform } from 'react-native';

// 🔧 Configuração dinâmica do URL do backend
const getApiUrl = () => {
  // Verifica se está a correr em plataforma nativa (iOS/Android)
  // vs web (browser)
  
  if (Platform.OS === 'web') {
    // Modo Web (browser) - usa localhost
    console.log('🌐 Plataforma: WEB');
    return 'http://localhost:8000';
  } else {
    // Modo Nativo (iOS/Android/Expo Go) - usa o IP da tua máquina
    console.log('📱 Plataforma: NATIVE (' + Platform.OS + ')');
    
    // ⚠️ IMPORTANTE: Este IP tem que ser o IP da tua máquina na rede local
    // Para encontrar: ipconfig (Windows) ou ifconfig (Mac/Linux)
    return 'http://192.168.1.64:8000';
  }
};

const API_URL = getApiUrl();

console.log('🌐 API URL configurado:', API_URL);

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_id: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
}

export const chatAPI = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    console.log('📤 A enviar mensagem para:', `${API_URL}/api/chat`);
    
    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Erro HTTP:', response.status, errorText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Resposta recebida com sucesso');
      return data;
    } catch (error) {
      console.error('❌ Erro ao fazer pedido:', error);
      throw error;
    }
  },
  
  // Método de teste para verificar conectividade
  testConnection: async (): Promise<boolean> => {
    console.log('🔍 A testar conexão com:', `${API_URL}/health`);
    try {
      const response = await fetch(`${API_URL}/health`, {
        method: 'GET',
      });
      console.log('✅ Teste de conexão:', response.ok ? 'SUCESSO' : 'FALHOU');
      return response.ok;
    } catch (error) {
      console.error('❌ Erro ao testar conexão:', error);
      return false;
    }
  }
};