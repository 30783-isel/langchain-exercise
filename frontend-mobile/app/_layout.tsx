import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import 'react-native-reanimated';

import { useColorScheme } from '@/hooks/use-color-scheme';
import { setupNetworkListener } from '@/utils/apiConfig';
import { chatAPI } from '@/services/api';

export const unstable_settings = {
  anchor: '(tabs)',
};

export default function RootLayout() {
  const colorScheme = useColorScheme();

  // 🌐 Configura listener de mudança de rede
  useEffect(() => {
    console.log('🚀 A configurar listener de rede...');
    
    const unsubscribe = setupNetworkListener(async () => {
      console.log('🔔 Rede mudou! A atualizar configuração da API...');
      
      try {
        // Força refresh do URL da API
        const newUrl = await chatAPI.refreshConfig();
        console.log('✅ Nova URL da API:', newUrl);
      } catch (error) {
        console.error('❌ Erro ao atualizar configuração:', error);
      }
    });
    
    // Cleanup quando o componente desmonta
    return () => {
      console.log('🔌 A desligar listener de rede');
      unsubscribe();
    };
  }, []); // Array vazio = executa apenas uma vez

  return (
    <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="modal" options={{ presentation: 'modal', title: 'Modal' }} />
      </Stack>
      <StatusBar style="auto" />
    </ThemeProvider>
  );
}