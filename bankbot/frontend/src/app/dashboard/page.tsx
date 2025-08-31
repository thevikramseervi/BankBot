'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Building2, MessageCircle, Bell, Settings, LogOut,
  CreditCard, TrendingUp, TrendingDown, Eye, EyeOff,
  ArrowUpRight, ArrowDownRight, Plus, Search
} from 'lucide-react';

interface Account {
  id: number;
  account_number: string;
  account_type: string;
  balance: number;
}

interface Transaction {
  id: number;
  transaction_type: string;
  amount: number;
  description: string;
  category: string;
  timestamp: string;
}

export default function Dashboard() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [totalBalance, setTotalBalance] = useState(0);
  const [showBalance, setShowBalance] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        // Redirect to login if no token
        window.location.href = '/';
        return;
      }

      // Fetch accounts and balance
      const balanceResponse = await fetch('http://localhost:8000/api/banking/balance', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (balanceResponse.ok) {
        const balanceData = await balanceResponse.json();
        setAccounts(balanceData.accounts);
        setTotalBalance(balanceData.total_balance);
      }

      // Fetch transactions
      const transactionsResponse = await fetch('http://localhost:8000/api/banking/transactions?limit=10', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (transactionsResponse.ok) {
        const transactionsData = await transactionsResponse.json();
        setTransactions(transactionsData);
      }

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'transactions', label: 'Transactions', icon: '💳' },
    { id: 'analytics', label: 'Analytics', icon: '📈' },
    { id: 'goals', label: 'Goals', icon: '🎯' },
    { id: 'settings', label: 'Settings', icon: '⚙️' }
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
                <Building2 className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">BankBot</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors">
                <MessageCircle className="h-5 w-5" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors">
                <Bell className="h-5 w-5" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors">
                <Settings className="h-5 w-5" />
              </button>
              <button
                onClick={handleLogout}
                className="p-2 text-gray-400 hover:text-red-600 transition-colors"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Account Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl p-8 text-white">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-semibold mb-2">Total Balance</h2>
                <div className="flex items-center space-x-3">
                  <span className="text-4xl font-bold">
                    {showBalance ? `$${totalBalance.toLocaleString()}` : '••••••'}
                  </span>
                  <button
                    onClick={() => setShowBalance(!showBalance)}
                    className="p-2 hover:bg-white/20 rounded-xl transition-colors"
                  >
                    {showBalance ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>
              <div className="text-right">
                <p className="text-blue-100 text-sm">Monthly Income</p>
                <p className="text-2xl font-semibold">+$2,450</p>
                <div className="flex items-center text-green-300 text-sm">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  +12.5%
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {accounts.map((account) => (
                <div key={account.id} className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-blue-100 text-sm capitalize">{account.account_type}</span>
                    <span className="text-xs text-blue-200">••••{account.account_number.slice(-4)}</span>
                  </div>
                  <p className="text-xl font-semibold">${account.balance.toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Navigation Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-8"
        >
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-2">
            <div className="flex space-x-2">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-xl font-medium transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-blue-500 text-white shadow-md'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="space-y-6"
        >
          {activeTab === 'overview' && (
            <>
              {/* Quick Actions */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Quick Transfer</h3>
                    <ArrowUpRight className="h-6 w-6 text-blue-500" />
                  </div>
                  <p className="text-gray-600 mb-4">Send money to friends and family instantly</p>
                  <button className="w-full bg-blue-500 text-white py-3 px-4 rounded-xl hover:bg-blue-600 transition-colors font-medium">
                    Transfer Now
                  </button>
                </div>

                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Pay Bills</h3>
                    <ArrowDownRight className="h-6 w-6 text-green-500" />
                  </div>
                  <p className="text-gray-600 mb-4">Pay your bills and utilities on time</p>
                  <button className="w-full bg-green-500 text-white py-3 px-4 rounded-xl hover:bg-green-600 transition-colors font-medium">
                    Pay Bills
                  </button>
                </div>

                <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Open Account</h3>
                    <Plus className="h-6 w-6 text-purple-500" />
                  </div>
                  <p className="text-gray-600 mb-4">Open a new savings or investment account</p>
                  <button className="w-full bg-purple-500 text-white py-3 px-4 rounded-xl hover:bg-purple-600 transition-colors font-medium">
                    Open Account
                  </button>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-semibold text-gray-900">Recent Activity</h3>
                  <button className="text-blue-500 hover:text-blue-600 font-medium">View All</button>
                </div>
                
                <div className="space-y-4">
                  {transactions.slice(0, 5).map((transaction) => (
                    <div key={transaction.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                      <div className="flex items-center space-x-4">
                        <div className={`p-3 rounded-full ${
                          transaction.transaction_type === 'credit' 
                            ? 'bg-green-100 text-green-600' 
                            : 'bg-red-100 text-red-600'
                        }`}>
                          {transaction.transaction_type === 'credit' ? (
                            <TrendingUp className="h-5 w-5" />
                          ) : (
                            <TrendingDown className="h-5 w-5" />
                          )}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{transaction.description}</p>
                          <p className="text-sm text-gray-500 capitalize">{transaction.category}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`font-semibold ${
                          transaction.transaction_type === 'credit' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {transaction.transaction_type === 'credit' ? '+' : '-'}${transaction.amount.toLocaleString()}
                        </p>
                        <p className="text-sm text-gray-500">
                          {new Date(transaction.timestamp).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {activeTab === 'transactions' && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-gray-900">All Transactions</h3>
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <Search className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search transactions..."
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <button className="bg-blue-500 text-white px-4 py-2 rounded-xl hover:bg-blue-600 transition-colors">
                    Export
                  </button>
                </div>
              </div>
              
              <div className="space-y-4">
                {transactions.map((transaction) => (
                  <div key={transaction.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center space-x-4">
                      <div className={`p-3 rounded-full ${
                        transaction.transaction_type === 'credit' 
                          ? 'bg-green-100 text-green-600' 
                          : 'bg-red-100 text-red-600'
                      }`}>
                        {transaction.transaction_type === 'credit' ? (
                          <TrendingUp className="h-5 w-5" />
                        ) : (
                          <TrendingDown className="h-5 w-5" />
                        )}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{transaction.description}</p>
                        <p className="text-sm text-gray-500 capitalize">{transaction.category}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`font-semibold ${
                        transaction.transaction_type === 'credit' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {transaction.transaction_type === 'credit' ? '+' : '-'}${transaction.amount.toLocaleString()}
                      </p>
                      <p className="text-sm text-gray-500">
                        {new Date(transaction.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'analytics' && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Financial Analytics</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl text-white">
                  <h4 className="text-lg font-semibold mb-2">Spending by Category</h4>
                  <p className="text-blue-100">Coming soon...</p>
                </div>
                <div className="p-6 bg-gradient-to-r from-green-500 to-teal-600 rounded-2xl text-white">
                  <h4 className="text-lg font-semibold mb-2">Income vs Expenses</h4>
                  <p className="text-green-100">Coming soon...</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'goals' && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Financial Goals</h3>
              <p className="text-gray-600">Goal setting features coming soon...</p>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Account Settings</h3>
              <p className="text-gray-600">Settings features coming soon...</p>
            </div>
          )}
        </motion.div>
      </main>
    </div>
  );
}