'use client'
import { useState } from 'react'
import axios from 'axios'

// Adiciona esta interface
interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function Home() {
  // Especifica o tipo aqui
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return
    
    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: input,
        conversation_id: 'session-123'
      })

      const aiMsg: Message = { role: 'assistant', content: response.data.response }
      setMessages(prev => [...prev, aiMsg])
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
      setInput('')
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">🪙 Crypto Intelligence</h1>
      
      <div className="chat-container bg-gray-100 p-4 rounded h-96 overflow-y-auto mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded ${
              msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300'
            }`}>
              {msg.content}
            </span>
          </div>
        ))}
        {loading && <div>A pensar...</div>}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Pergunta sobre crypto..."
          className="flex-1 p-2 border rounded"
        />
        <button 
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Enviar
        </button>
      </div>
    </div>
  )
}