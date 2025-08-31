'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Building2, MessageCircle, LogOut, CreditCard, TrendingUp, 
  ArrowUpRight, ArrowDownRight, DollarSign, Users, Shield,
  BarChart3, PieChart, Activity, Calendar, Filter,
  Search, Plus, Download, Eye, EyeOff, Bell, Settings,
  Wallet, PiggyBank, Investment, Zap, Target, Award
} from 'lucide-react';

interface Transaction {
  id: number;
  type: 'credit' | 'debit';
  amount: number;
  description: string;
  date: string;
  category: string;
  icon: string;
  status: 'completed' | 'pending' | 'failed';
}

interface Account {
  id: number;
  name: string;
  number: string;
  balance: number;
  type: 'checking' | 'savings' | 'investment';
  color: string;
  trend: 'up' | 'down' | 'stable';
  change: number;
}

export default function Dashboard() {
  const [showBalance, setShowBalance] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const accounts: Account[] = [
    { 
      id: 1, 
      name: 'Main Checking', 
      number: '****1234', 
      balance: 1234.56, 
      type: 'checking', 
      color: 'from-blue-500 to-blue-600',
      trend: 'up',
      change: 2.5
    },
    { 
      id: 2, 
      name: 'Savings', 
      number: '****5678', 
      balance: 1216.11, 
      type: 'savings', 
      color: 'from-green-500 to-green-600',
      trend: 'up',
      change: 1.8
    },
    { 
      id: 3, 
      name: 'Investment', 
      number: '****9012', 
      balance: 5678.90, 
      type: 'investment', 
      color: 'from-purple-500 to-purple-600',
      trend: 'up',
      change: 5.2
    }
  ];

  const transactions: Transaction[] = [
    { id: 1, type: 'debit', amount: -45.67, description: 'Coffee Shop', date: '2024-01-15', category: 'Food & Dining', icon: '☕', status: 'completed' },
    { id: 2, type: 'credit', amount: 2500.00, description: 'Salary Deposit', date: '2024-01-14', category: 'Income', icon: '💰', status: 'completed' },
    { id: 3, type: 'debit', amount: -89.99, description: 'Online Store', date: '2024-01-13', category: 'Shopping', icon: '🛍️', status: 'completed' },
    { id: 4, type: 'credit', amount: 150.00, description: 'Refund', date: '2024-01-12', category: 'Refund', icon: '↩️', status: 'pending' },
    { id: 5, type: 'debit', amount: -23.45, description: 'Gas Station', date: '2024-01-11', category: 'Transportation', icon: '⛽', status: 'completed' }
  ];

  const totalBalance = accounts.reduce((sum, account) => sum + account.balance, 0);
  const monthlyIncome = transactions.filter(t => t.type === 'credit').reduce((sum, t) => sum + t.amount, 0);
  const monthlyExpenses = Math.abs(transactions.filter(t => t.type === 'debit').reduce((sum, t) => sum + t.amount, 0));

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-500';
      case 'pending': return 'text-yellow-500';
      case 'failed': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✓';
      case 'pending': return '⏳';
      case 'failed': return '✗';
      default: return '•';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/80 backdrop-blur-md border-b border-white/20 shadow-sm sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-3"
            >
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
                <Building2 className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-blue-600 bg-clip-text text-transparent">
                BankBot Dashboard
              </h1>
            </motion.div>
            
            <div className="flex items-center space-x-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsChatbotOpen(true)}
                className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                <MessageCircle className="h-5 w-5" />
                <span>Chat with BankBot</span>
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-slate-600 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100"
              >
                <Bell className="h-5 w-5" />
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-slate-600 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100"
              >
                <Settings className="h-5 w-5" />
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center space-x-2 text-slate-600 hover:text-slate-800 transition-colors p-2 rounded-lg hover:bg-slate-100"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </motion.button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Balance Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <div className="bg-white rounded-3xl shadow-xl p-8 border border-white/20">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-slate-800">Account Overview</h2>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowBalance(!showBalance)}
                className="p-2 text-slate-600 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100"
              >
                {showBalance ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </motion.button>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="text-center p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl border border-blue-200"
              >
                <div className="text-3xl font-bold text-slate-800 mb-2">
                  {showBalance ? `$${totalBalance.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                </div>
                <div className="text-slate-600">Total Balance</div>
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="text-center p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl border border-green-200"
              >
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {showBalance ? `$${monthlyIncome.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                </div>
                <div className="text-slate-600">Monthly Income</div>
              </motion.div>
              
              <motion.div
                whileHover={{ scale: 1.02 }}
                className="text-center p-6 bg-gradient-to-r from-red-50 to-pink-50 rounded-2xl border border-red-200"
              >
                <div className="text-3xl font-bold text-red-600 mb-2">
                  {showBalance ? `$${monthlyExpenses.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                </div>
                <div className="text-slate-600">Monthly Expenses</div>
              </motion.div>
            </div>

            {/* Account Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {accounts.map((account, index) => (
                <motion.div
                  key={account.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                  className="bg-gradient-to-r from-slate-50 to-slate-100 rounded-2xl p-6 border border-slate-200 hover:shadow-lg transition-all duration-300"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-3 rounded-xl bg-gradient-to-r ${account.color}`}>
                      <CreditCard className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-slate-500 capitalize">{account.type}</span>
                      <div className={`flex items-center space-x-1 text-sm ${
                        account.trend === 'up' ? 'text-green-600' : 
                        account.trend === 'down' ? 'text-red-600' : 'text-slate-600'
                      }`}>
                        {account.trend === 'up' ? <ArrowUpRight className="h-4 w-4" /> : 
                         account.trend === 'down' ? <ArrowDownRight className="h-4 w-4" /> : 
                         <div className="w-4 h-4" />}
                        <span>{account.change}%</span>
                      </div>
                    </div>
                  </div>
                  <h3 className="font-semibold text-slate-800 mb-2">{account.name}</h3>
                  <p className="text-slate-600 text-sm mb-3">{account.number}</p>
                  <div className="text-2xl font-bold text-slate-800">
                    {showBalance ? `$${account.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '****'}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="bg-white rounded-3xl shadow-xl border border-white/20 overflow-hidden"
        >
          <div className="border-b border-slate-200">
            <nav className="flex space-x-8 px-8">
              {[
                { id: 'overview', label: 'Overview', icon: BarChart3 },
                { id: 'transactions', label: 'Transactions', icon: Activity },
                { id: 'analytics', label: 'Analytics', icon: PieChart },
                { id: 'goals', label: 'Goals', icon: Target },
                { id: 'settings', label: 'Settings', icon: Settings }
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <motion.button
                    key={tab.id}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{tab.label}</span>
                  </motion.button>
                );
              })}
            </nav>
          </div>

          <div className="p-8">
            <AnimatePresence mode="wait">
              {activeTab === 'overview' && (
                <motion.div
                  key="overview"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <motion.div
                      whileHover={{ scale: 1.02 }}
                      className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200"
                    >
                      <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
                        <Zap className="h-5 w-5 mr-2 text-blue-600" />
                        Quick Actions
                      </h3>
                      <div className="space-y-3">
                        {[
                          { label: 'Transfer Money', icon: ArrowUpRight, color: 'text-blue-600' },
                          { label: 'Pay Bills', icon: ArrowUpRight, color: 'text-blue-600' },
                          { label: 'Open New Account', icon: Plus, color: 'text-blue-600' }
                        ].map((action, index) => (
                          <motion.button
                            key={index}
                            whileHover={{ x: 5 }}
                            className="w-full flex items-center justify-between p-3 bg-white rounded-xl border border-blue-200 hover:shadow-md transition-all duration-200"
                          >
                            <span className="text-slate-700">{action.label}</span>
                            <action.icon className={`h-5 w-5 ${action.color}`} />
                          </motion.button>
                        ))}
                      </div>
                    </motion.div>
                    
                    <motion.div
                      whileHover={{ scale: 1.02 }}
                      className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-200"
                    >
                      <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center">
                        <Activity className="h-5 w-5 mr-2 text-green-600" />
                        Recent Activity
                      </h3>
                      <div className="space-y-3">
                        {transactions.slice(0, 3).map((transaction) => (
                          <motion.div
                            key={transaction.id}
                            whileHover={{ x: 5 }}
                            className="flex items-center space-x-3 p-2"
                          >
                            <span className="text-2xl">{transaction.icon}</span>
                            <div className="flex-1">
                              <p className="text-sm font-medium text-slate-700">{transaction.description}</p>
                              <p className="text-xs text-slate-500">{transaction.date}</p>
                            </div>
                            <span className={`font-semibold ${transaction.type === 'credit' ? 'text-green-600' : 'text-red-600'}`}>
                              {transaction.type === 'credit' ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                            </span>
                          </motion.div>
                        ))}
                      </div>
                    </motion.div>
                  </div>
                </motion.div>
              )}

              {activeTab === 'transactions' && (
                <motion.div
                  key="transactions"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
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
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="p-2 text-slate-600 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100"
                      >
                        <Filter className="h-5 w-5" />
                      </motion.button>
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="p-2 text-slate-600 hover:text-slate-800 transition-colors rounded-lg hover:bg-slate-100"
                      >
                        <Download className="h-5 w-5" />
                      </motion.button>
                    </div>
                  </div>

                  <div className="space-y-3">
                    {transactions.map((transaction, index) => (
                      <motion.div
                        key={transaction.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.05 }}
                        whileHover={{ scale: 1.01, x: 5 }}
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
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-slate-500 capitalize">{transaction.type}</span>
                            <span className={`text-sm ${getStatusColor(transaction.status)}`}>
                              {getStatusIcon(transaction.status)}
                            </span>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}

              {activeTab === 'analytics' && (
                <motion.div
                  key="analytics"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="text-center py-12"
                >
                  <div className="text-6xl mb-4">📊</div>
                  <h3 className="text-xl font-semibold text-slate-800 mb-2">Analytics Dashboard</h3>
                  <p className="text-slate-600">Detailed financial insights and spending patterns coming soon!</p>
                </motion.div>
              )}

              {activeTab === 'goals' && (
                <motion.div
                  key="goals"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="text-center py-12"
                >
                  <div className="text-6xl mb-4">🎯</div>
                  <h3 className="text-xl font-semibold text-slate-800 mb-2">Financial Goals</h3>
                  <p className="text-slate-600">Set and track your financial goals with smart insights!</p>
                </motion.div>
              )}

              {activeTab === 'settings' && (
                <motion.div
                  key="settings"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="text-center py-12"
                >
                  <div className="text-6xl mb-4">⚙️</div>
                  <h3 className="text-xl font-semibold text-slate-800 mb-2">Account Settings</h3>
                  <p className="text-slate-600">Manage your preferences and security settings here.</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </main>

      {/* Chatbot Modal */}
      <AnimatePresence>
        {isChatbotOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-3xl shadow-2xl w-full max-w-md h-[600px] flex flex-col overflow-hidden"
            >
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-3xl">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-white/20 rounded-xl">
                      <MessageCircle className="h-6 w-6" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold">BankBot</h3>
                      <p className="text-sm text-blue-100">AI Banking Assistant</p>
                    </div>
                  </div>
                  <button
                    onClick={() => setIsChatbotOpen(false)}
                    className="p-2 hover:bg-white/20 rounded-xl transition-colors"
                  >
                    ✕
                  </button>
                </div>
              </div>
              
              <div className="flex-1 p-6 bg-gradient-to-b from-slate-50 to-white">
                <div className="text-center py-8">
                  <div className="text-4xl mb-4">🤖</div>
                  <h4 className="text-lg font-semibold text-slate-800 mb-2">Chat with BankBot</h4>
                  <p className="text-slate-600">Ask me anything about your banking!</p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}