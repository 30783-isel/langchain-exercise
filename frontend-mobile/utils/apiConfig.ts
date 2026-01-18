import * as Network from 'expo-network';
import { Platform } from 'react-native';

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
 * Obtém o URL da API baseado no ambiente
 */
export async function getApiUrl() {
  const connection = await detectConnectionType();
  
  // URLs configurados
  const TAILSCALE_API = 'http://100.100.94.97:8000'; 
  const LOCAL_API = 'http://192.168.1.64:8000';  
  const LOCALHOST_API = 'http://localhost:8000';
  
  // Lógica de seleção
  if (connection.isTailscale) {
    console.log('🔐 Usando Tailscale API');
    return TAILSCALE_API;
  }
  
  if (Platform.OS === 'web') {
    console.log('🌐 Usando Localhost (Web)');
    return LOCALHOST_API;
  }
  
  console.log('🏠 Usando Local Network API');
  return LOCAL_API;
}