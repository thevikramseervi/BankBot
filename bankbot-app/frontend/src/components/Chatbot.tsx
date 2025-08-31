'use client';

import { useState, useEffect, useRef } from 'react';
import { Send, Bot, X, Sparkles, MessageCircle, CreditCard, TrendingUp, Shield } from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
  intent?: string;
  confidence?: number;
  entities?: any;
}

interface ChatbotProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function Chatbot({ isOpen, onClose }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      content: "Hi! I'm BankBot, your AI banking assistant. I can help you with balance inquiries, transfers, transactions, and more. What would you like to know?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!sessionId) {
      setSessionId(Math.random().toString(36).substring(7));
    }
  }, [sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'bot',
          content: data.response,
          timestamp: new Date(),
          intent: data.intent_detected,
          confidence: data.confidence_score,
          entities: data.entities
        };

        setMessages(prev => [...prev, botMessage]);
      } else {
        const fallbackMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'bot',
          content: "I'm sorry, I'm having trouble connecting right now. Please try again later or contact customer support.",
          timestamp: new Date()
        };
        setMessages(prev => [...prev, fallbackMessage]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: "I'm experiencing technical difficulties. Please try again in a moment.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const quickReplies = [
    { text: "What's my balance?", icon: CreditCard, color: "from-blue-500 to-blue-600" },
    { text: "How do I transfer money?", icon: TrendingUp, color: "from-green-500 to-green-600" },
    { text: "Show my transactions", icon: MessageCircle, color: "from-purple-500 to-purple-600" },
    { text: "Account information", icon: Shield, color: "from-orange-500 to-orange-600" }
  ];

  const handleQuickReply = (reply: string) => {
    setInputMessage(reply);
    setTimeout(() => handleSendMessage(), 100);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md h-[600px] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-3xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-white/20 rounded-xl">
                <Bot className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-semibold">BankBot</h3>
                <p className="text-sm text-blue-100">AI Banking Assistant</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/20 rounded-xl transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-slate-50 to-white">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl shadow-sm ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-br-md'
                    : 'bg-white border border-slate-200 text-slate-800 rounded-bl-md'
                }`}
              >
                <p className="text-sm leading-relaxed">{message.content}</p>
                {message.intent && (
                  <div className="mt-2 text-xs opacity-75 flex items-center space-x-1">
                    <Sparkles className="h-3 w-3" />
                    <span>Intent: {message.intent}</span>
                    {message.confidence && (
                      <span>({(message.confidence * 100).toFixed(1)}%)</span>
                    )}
                  </div>
                )}
                {message.entities && Object.keys(message.entities).length > 0 && (
                  <div className="mt-2 text-xs opacity-75">
                    <span className="font-medium">Entities:</span> {Object.keys(message.entities).map((key) => `${key}: ${message.entities[key]}`).join(', ')}
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-white border border-slate-200 text-slate-800 px-4 py-3 rounded-2xl rounded-bl-md shadow-sm">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Replies */}
        <div className="px-6 pb-4 bg-white border-t border-slate-100">
          <div className="flex flex-wrap gap-2 mb-4">
            {quickReplies.map((reply, index) => {
              const Icon = reply.icon;
              return (
                <button
                  key={index}
                  onClick={() => handleQuickReply(reply.text)}
                  className="flex items-center space-x-2 bg-gradient-to-r from-slate-100 to-slate-200 text-slate-700 px-3 py-2 rounded-full hover:from-slate-200 hover:to-slate-300 transition-all duration-200 text-xs font-medium"
                >
                  <Icon className="h-3 w-3" />
                  <span>{reply.text}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Input */}
        <div className="p-6 bg-white border-t border-slate-100">
          <div className="flex space-x-3">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all duration-200 placeholder-slate-400"
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isTyping}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}