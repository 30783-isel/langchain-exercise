// frontend-mobile/utils/apiConfig.ts
import * as Network from 'expo-network';
import { Platform } from 'react-native';
import NetInfo from '@react-native-community/netinfo';

let cachedApiUrl: string | null = null;
let cachedConnectionType: string | null = null;

/**
 * Deteta se estamos a usar Tailscale baseado no IP local
 */
export async function detectConnectionType() {
  try {
    const ip = await Network.getIpAddressAsync();
    
    // IPs Tailscale: 100.64.0.0 até 100.127.255.255
    const isTailscale = ip.startsWith('100.') && 
                        parseInt(ip.split('.')[1]) >= 64 && 
                        parseInt(ip.split('.')[1]) <= 127;
    
    console.log(`📱 IP Detetado: ${ip}`);
    console.log(`🔐 É Tailscale: ${isTailscale}`);
    
    return {
      clientIp: ip,
      isTailscale,
      connectionType: isTailscale ? 'tailscale' : 'local/mobile'
    };
  } catch (error) {
    console.error('Error detecting connection:', error);
    return {
      clientIp: 'unknown',
      isTailscale: false,
      connectionType: 'unknown'
    };
  }
}

/**
 * Obtém o URL da API baseado no ambiente (com forçar refresh)
 */
export async function getApiUrl(forceRefresh: boolean = false): Promise<string> {
  // Se forçar refresh, limpa o cache
  if (forceRefresh) {
    console.log('🔄 A forçar refresh do URL da API...');
    cachedApiUrl = null;
    cachedConnectionType = null;
  }

  // Se já temos cache, retorna
  if (cachedApiUrl && !forceRefresh) {
    console.log('💾 Usando URL do cache:', cachedApiUrl);
    return cachedApiUrl;
  }

  const connection = await detectConnectionType();
  
  // URLs configurados
  const TAILSCALE_API = 'http://100.100.94.97:8000'; 
  const LOCAL_API = 'http://192.168.1.130:8000';  
  const LOCALHOST_API = 'http://localhost:8000';
  
  let selectedUrl: string;
  
  // Lógica de seleção
  if (connection.isTailscale) {
    console.log('🔐 Usando Tailscale API');
    selectedUrl = TAILSCALE_API;
  } else if (Platform.OS === 'web') {
    console.log('🌐 Usando Localhost (Web)');
    selectedUrl = LOCALHOST_API;
  } else {
    console.log('🏠 Usando Local Network API');
    selectedUrl = LOCAL_API;
  }
  
  cachedApiUrl = selectedUrl;
  cachedConnectionType = connection.connectionType;
  
  console.log(`✅ URL configurado: ${cachedApiUrl} (${cachedConnectionType})`);
  
  return cachedApiUrl;
}

/**
 * Invalida o cache do URL (chamar quando a rede muda)
 */
export function invalidateCache() {
  console.log('🗑️ Cache invalidado');
  cachedApiUrl = null;
  cachedConnectionType = null;
}

/**
 * Configura listener para mudanças de rede
 */
export function setupNetworkListener(onNetworkChange?: () => void) {
  console.log('📡 A configurar listener de rede...');
  
  const unsubscribe = NetInfo.addEventListener(state => {
    console.log('\n🔔 Mudança de rede detetada!');
    console.log(`   Tipo: ${state.type}`);
    console.log(`   Conectado: ${state.isConnected}`);
    console.log(`   Internet: ${state.isInternetReachable}`);
    
    // Invalida o cache quando a rede muda
    invalidateCache();
    
    // Callback opcional
    if (onNetworkChange) {
      onNetworkChange();
    }
  });
  
  return unsubscribe;
}