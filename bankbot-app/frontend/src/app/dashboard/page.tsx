'use client';

import { useState } from 'react';
import { Building2, MessageCircle, LogOut } from 'lucide-react';
import Chatbot from '@/components/Chatbot';

export default function Dashboard() {
  const [showChatbot, setShowChatbot] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <Building2 className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">BankBot Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowChatbot(true)}
                className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                <MessageCircle className="h-5 w-5" />
                <span>Chat with BankBot</span>
              </button>
              <button className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors">
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Welcome to BankBot!</h2>
          <p className="text-xl text-gray-600 mb-8">
            Your AI-powered banking assistant is ready to help.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-blue-50 rounded-lg">
              <h3 className="text-lg font-semibold text-blue-900 mb-2">Check Balance</h3>
              <p className="text-blue-700">Ask BankBot about your account balance</p>
            </div>
            <div className="p-6 bg-green-50 rounded-lg">
              <h3 className="text-lg font-semibold text-green-900 mb-2">Transfer Money</h3>
              <p className="text-green-700">Get help with money transfers</p>
            </div>
            <div className="p-6 bg-purple-50 rounded-lg">
              <h3 className="text-lg font-semibold text-purple-900 mb-2">Transaction History</h3>
              <p className="text-purple-700">View your recent transactions</p>
            </div>
          </div>
        </div>
      </main>

      {/* Chatbot */}
      <Chatbot isOpen={showChatbot} onClose={() => setShowChatbot(false)} />
    </div>
  );
}