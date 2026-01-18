// frontend-mobile/services/api.ts
import { getApiUrl, invalidateCache } from '@/utils/apiConfig';

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
    const API_URL = await getApiUrl(); // ✅ Sempre pega o URL mais recente
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
      
      // 🔄 RETRY com refresh do URL em caso de erro
      console.log('🔄 A tentar novamente com refresh do URL...');
      const newApiUrl = await getApiUrl(true); // Force refresh
      
      try {
        const retryResponse = await fetch(`${newApiUrl}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request),
        });
        
        if (!retryResponse.ok) {
          throw new Error(`HTTP error! status: ${retryResponse.status}`);
        }
        
        const retryData = await retryResponse.json();
        console.log('✅ Retry bem-sucedido!');
        return retryData;
      } catch (retryError) {
        console.error('❌ Retry também falhou:', retryError);
        throw error; // Lança o erro original
      }
    }
  },
  
  testConnection: async (): Promise<boolean> => {
    const API_URL = await getApiUrl();
    console.log('🔍 A testar conexão com:', `${API_URL}/health`);
    
    try {
      const response = await fetch(`${API_URL}/health`, {
        method: 'GET'
      });
      console.log('✅ Teste de conexão:', response.ok ? 'SUCESSO' : 'FALHOU');
      return response.ok;
    } catch (error) {
      console.error('❌ Erro ao testar conexão:', error);
      return false;
    }
  },
  
  // Força refresh da configuração manualmente
  refreshConfig: async (): Promise<string> => {
    console.log('🔄 A forçar refresh manual...');
    invalidateCache();
    return await getApiUrl(true);
  }
};