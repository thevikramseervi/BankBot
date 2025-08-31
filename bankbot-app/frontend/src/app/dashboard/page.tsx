'use client';

import { useState, useEffect } from 'react';
import { 
  Building2, MessageCircle, LogOut, CreditCard, TrendingUp, 
  ArrowUpRight, ArrowDownRight, DollarSign, Users, Shield,
  BarChart3, PieChart, Activity, Calendar, Filter,
  Search, Plus, Download, Eye, EyeOff
} from 'lucide-react';
import Chatbot from '@/components/Chatbot';

interface Transaction {
  id: number;
  type: 'credit' | 'debit';
  amount: number;
  description: string;
  date: string;
  category: string;
  icon: string;
}

interface Account {
  id: number;
  name: string;
  number: string;
  balance: number;
  type: 'checking' | 'savings';
  color: string;
}

export default function Dashboard() {
  const [showChatbot, setShowChatbot] = useState(false);
  const [showBalance, setShowBalance] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  const accounts: Account[] = [
    { id: 1, name: 'Main Checking', number: '****1234', balance: 1234.56, type: 'checking', color: 'from-blue-500 to-blue-600' },
    { id: 2, name: 'Savings', number: '****5678', balance: 1216.11, type: 'savings', color: 'from-green-500 to-green-600' },
    { id: 3, name: 'Investment', number: '****9012', balance: 5678.90, type: 'savings', color: 'from-purple-500 to-purple-600' }
  ];

  const transactions: Transaction[] = [
    { id: 1, type: 'debit', amount: -45.67, description: 'Coffee Shop', date: '2024-01-15', category: 'Food & Dining', icon: '☕' },
    { id: 2, type: 'credit', amount: 2500.00, description: 'Salary Deposit', date: '2024-01-14', category: 'Income', icon: '💰' },
    { id: 3, type: 'debit', amount: -89.99, description: 'Online Store', date: '2024-01-13', category: 'Shopping', icon: '🛍️' },
    { id: 4, type: 'credit', amount: 150.00, description: 'Refund', date: '2024-01-12', category: 'Refund', icon: '↩️' },
    { id: 5, type: 'debit', amount: -23.45, description: 'Gas Station', date: '2024-01-11', category: 'Transportation', icon: '⛽' }
  ];

  const totalBalance = accounts.reduce((sum, account) => sum + account.balance, 0);
  const monthlyIncome = transactions.filter(t => t.type === 'credit').reduce((sum, t) => sum + t.amount, 0);
  const monthlyExpenses = Math.abs(transactions.filter(t => t.type === 'debit').reduce((sum, t) => sum + t.amount, 0));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-white/20 shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
                <Building2 className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-blue-600 bg-clip-text text-transparent">
                BankBot Dashboard
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowChatbot(true)}
                className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                <MessageCircle className="h-5 w-5" />
                <span>Chat with BankBot</span>
              </button>
              <button className="flex items-center space-x-2 text-slate-600 hover:text-slate-800 transition-colors p-2 rounded-lg hover:bg-slate-100">
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Balance Overview */}
        <div className="mb-8">
          <div className="bg-white rounded-3xl shadow-xl p-8 border border-white/20">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-slate-800">Account Overview</h2>
              <button
                onClick={() => setShowBalance(!showBalance)}
                className="p-2 text-slate-600 hover:text-slate-800 transition-colors"
              >
                {showBalance ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-slate-800 mb-2">
                  {showBalance ? `$${totalBalance.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                </div>
                <div className="text-slate-600">Total Balance</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {showBalance ? `$${monthlyIncome.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                </div>
                <div className="text-slate-600">Monthly Income</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-red-600 mb-2">
                  {showBalance ? `$${monthlyExpenses.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                </div>
                <div className="text-slate-600">Monthly Expenses</div>
              </div>
            </div>

            {/* Account Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {accounts.map((account) => (
                <div
                  key={account.id}
                  className="bg-gradient-to-r from-slate-50 to-slate-100 rounded-2xl p-6 border border-slate-200 hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-3 rounded-xl bg-gradient-to-r ${account.color}`>
                      <CreditCard className="h-6 w-6 text-white" />
                    </div>
                    <span className="text-sm text-slate-500 capitalize">{account.type}</span>
                  </div>
                  <h3 className="font-semibold text-slate-800 mb-2">{account.name}</h3>
                  <p className="text-slate-600 text-sm mb-3">{account.number}</p>
                  <div className="text-2xl font-bold text-slate-800">
                    {showBalance ? `$${account.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-3xl shadow-xl border border-white/20 overflow-hidden">
          <div className="border-b border-slate-200">
            <nav className="flex space-x-8 px-8">
              {[
                { id: 'overview', label: 'Overview', icon: BarChart3 },
                { id: 'transactions', label: 'Transactions', icon: Activity },
                { id: 'analytics', label: 'Analytics', icon: PieChart },
                { id: 'settings', label: 'Settings', icon: Shield }
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          <div className="p-8">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200">
                    <h3 className="text-lg font-semibold text-slate-800 mb-4">Quick Actions</h3>
                    <div className="space-y-3">
                      <button className="w-full flex items-center justify-between p-3 bg-white rounded-xl border border-blue-200 hover:shadow-md transition-all duration-200">
                        <span className="text-slate-700">Transfer Money</span>
                        <ArrowUpRight className="h-5 w-5 text-blue-600" />
                      </button>
                      <button className="w-full flex items-center justify-between p-3 bg-white rounded-xl border border-blue-200 hover:shadow-md transition-all duration-200">
                        <span className="text-slate-700">Pay Bills</span>
                        <ArrowUpRight className="h-5 w-5 text-blue-600" />
                      </button>
                      <button className="w-full flex items-center justify-between p-3 bg-white rounded-xl border border-blue-200 hover:shadow-md transition-all duration-200">
                        <span className="text-slate-700">Open New Account</span>
                        <ArrowUpRight className="h-5 w-5 text-blue-600" />
                      </button>
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-200">
                    <h3 className="text-lg font-semibold text-slate-800 mb-4">Recent Activity</h3>
                    <div className="space-y-3">
                      {transactions.slice(0, 3).map((transaction) => (
                        <div key={transaction.id} className="flex items-center space-x-3 p-2">
                          <span className="text-2xl">{transaction.icon}</span>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-slate-700">{transaction.description}</p>
                            <p className="text-xs text-slate-500">{transaction.date}</p>
                          </div>
                          <span className={`font-semibold ${transaction.type === 'credit' ? 'text-green-600' : 'text-red-600'}`}>
                            {transaction.type === 'credit' ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'transactions' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-slate-800">Transaction History</h3>
                  <div className="flex items-center space-x-3">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                      <input
                        type="text"
                        placeholder="Search transactions..."
                        className="pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <button className="p-2 text-slate-600 hover:text-slate-800 transition-colors">
                      <Filter className="h-5 w-5" />
                    </button>
                    <button className="p-2 text-slate-600 hover:text-slate-800 transition-colors">
                      <Download className="h-5 w-5" />
                    </button>
                  </div>
                </div>

                <div className="space-y-3">
                  {transactions.map((transaction) => (
                    <div
                      key={transaction.id}
                      className="flex items-center space-x-4 p-4 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors duration-200"
                    >
                      <div className="text-3xl">{transaction.icon}</div>
                      <div className="flex-1">
                        <h4 className="font-medium text-slate-800">{transaction.description}</h4>
                        <p className="text-sm text-slate-500">{transaction.category} • {transaction.date}</p>
                      </div>
                      <div className="text-right">
                        <div className={`font-semibold text-lg ${transaction.type === 'credit' ? 'text-green-600' : 'text-red-600'}`}>
                          {transaction.type === 'credit' ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                        </div>
                        <div className="text-sm text-slate-500 capitalize">{transaction.type}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'analytics' && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">📊</div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">Analytics Dashboard</h3>
                <p className="text-slate-600">Detailed financial insights and spending patterns coming soon!</p>
              </div>
            )}

            {activeTab === 'settings' && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">⚙️</div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">Account Settings</h3>
                <p className="text-slate-600">Manage your preferences and security settings here.</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Chatbot */}
      <Chatbot isOpen={showChatbot} onClose={() => setShowChatbot(false)} />
    </div>
  );
}