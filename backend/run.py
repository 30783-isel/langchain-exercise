import uvicorn

if __name__ == "__main__":
    print("🚀 A iniciar servidor backend...")
    print("📍 O servidor estará disponível em:")
    print("   • http://localhost:8000")
    print("   • http://127.0.0.1:8000")
    print("   • http://<teu-ip-local>:8000")
    print("\n💡 Para encontrar o teu IP local:")
    print("   • Mac/Linux: ifconfig | grep 'inet '")
    print("   • Windows: ipconfig")
    print("\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # ✅ CORRIGIDO: Aceita conexões de qualquer IP (não só 127.0.0.1)
        port=8000,
        reload=True
    )