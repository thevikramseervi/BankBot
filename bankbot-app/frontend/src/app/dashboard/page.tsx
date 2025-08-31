'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Building2, 
  MessageCircle, 
  LogOut, 
  CreditCard, 
  DollarSign, 
  TrendingUp, 
  Send,
  User,
  Settings,
  Plus
} from 'lucide-react';
import Chatbot from '@/components/Chatbot';
import TransferForm from '@/components/TransferForm';

interface Account {
  id: string;
  account_number: string;
  account_type: string;
  balance: string;
  is_active: boolean;
}

interface Transaction {
  id: string;
  transaction_type: string;
  amount: string;
  description: string;
  balance_after: string;
  reference_number: string;
  created_at: string;
}

interface Transfer {
  id: string;
  from_account: Account;
  to_account: Account;
  amount: string;
  description: string;
  status: string;
  created_at: string;
}

interface BankingStats {
  total_balance: string;
  account_count: number;
  recent_transactions: Transaction[];
  pending_transfers: number;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [transfers, setTransfers] = useState<Transfer[]>([]);
  const [stats, setStats] = useState<BankingStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showChatbot, setShowChatbot] = useState(false);
  const [showTransferForm, setShowTransferForm] = useState(false);
  const router = useRouter();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch accounts
      const accountsResponse = await fetch('http://localhost:8000/api/banking/accounts/', {
        credentials: 'include'
      });
      if (accountsResponse.ok) {
        const accountsData = await accountsResponse.json();
        setAccounts(accountsData);
      }

      // Fetch stats
      const statsResponse = await fetch('http://localhost:8000/api/banking/stats/summary/', {
        credentials: 'include'
      });
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }

      // Fetch recent transactions
      const transactionsResponse = await fetch('http://localhost:8000/api/banking/transactions/', {
        credentials: 'include'
      });
      if (transactionsResponse.ok) {
        const transactionsData = await transactionsResponse.json();
        setTransactions(transactionsData.slice(0, 10)); // Show last 10 transactions
      }

      // Fetch transfers
      const transfersResponse = await fetch('http://localhost:8000/api/banking/transfers/', {
        credentials: 'include'
      });
      if (transfersResponse.ok) {
        const transfersData = await transfersResponse.json();
        setTransfers(transfersData);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await fetch('http://localhost:8000/api/auth/logout/', {
        method: 'POST',
        credentials: 'include'
      });
      router.push('/');
    } catch (error) {
      console.error('Logout error:', error);
      router.push('/');
    }
  };

  const handleTransferSuccess = () => {
    fetchDashboardData(); // Refresh data after successful transfer
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your banking dashboard...</p>
        </div>
      </div>
    );
  }

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
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: TrendingUp },
              { id: 'accounts', label: 'Accounts', icon: CreditCard },
              { id: 'transactions', label: 'Transactions', icon: DollarSign },
              { id: 'transfers', label: 'Transfers', icon: Send },
              { id: 'profile', label: 'Profile', icon: User },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <tab.icon className="h-5 w-5" />
                  <span>{tab.label}</span>
                </div>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <DollarSign className="h-8 w-8 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Total Balance</p>
                    <p className="text-2xl font-semibold text-gray-900">
                      ${stats?.total_balance || '0.00'}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <CreditCard className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Active Accounts</p>
                    <p className="text-2xl font-semibold text-gray-900">
                      {stats?.account_count || 0}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <Send className="h-8 w-8 text-purple-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Pending Transfers</p>
                    <p className="text-2xl font-semibold text-gray-900">
                      {stats?.pending_transfers || 0}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Transactions */}
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Recent Transactions</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Type
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Amount
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Description
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {transactions.map((transaction) => (
                      <tr key={transaction.id}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            transaction.transaction_type === 'deposit' ? 'bg-green-100 text-green-800' :
                            transaction.transaction_type === 'withdrawal' ? 'bg-red-100 text-red-800' :
                            'bg-blue-100 text-blue-800'
                          }`}>
                            {transaction.transaction_type}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${parseFloat(transaction.amount).toFixed(2)}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {transaction.description}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(transaction.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Accounts Tab */}
        {activeTab === 'accounts' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-medium text-gray-900">Your Accounts</h3>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {accounts.map((account) => (
                    <div key={account.id} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-500">
                          {account.account_type.charAt(0).toUpperCase() + account.account_type.slice(1)}
                        </span>
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          account.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {account.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                      <p className="text-lg font-semibold text-gray-900">
                        ${parseFloat(account.balance).toFixed(2)}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        {account.account_number}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Transfers Tab */}
        {activeTab === 'transfers' && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">Money Transfers</h3>
                <button
                  onClick={() => setShowTransferForm(true)}
                  className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="h-5 w-5" />
                  <span>New Transfer</span>
                </button>
              </div>
              <div className="p-6">
                {transfers.length > 0 ? (
                  <div className="space-y-4">
                    {transfers.map((transfer) => (
                      <div key={transfer.id} className="border rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium text-gray-500">
                            Transfer #{transfer.id.slice(0, 8)}
                          </span>
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                            transfer.status === 'completed' ? 'bg-green-100 text-green-800' :
                            transfer.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {transfer.status.charAt(0).toUpperCase() + transfer.status.slice(1)}
                          </span>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <p className="text-sm text-gray-500">From</p>
                            <p className="font-medium">{transfer.from_account.account_number}</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">To</p>
                            <p className="font-medium">{transfer.to_account.account_number}</p>
                          </div>
                        </div>
                        <div className="mt-3 pt-3 border-t">
                          <div className="flex justify-between items-center">
                            <div>
                              <p className="text-lg font-semibold text-gray-900">
                                ${parseFloat(transfer.amount).toFixed(2)}
                              </p>
                              {transfer.description && (
                                <p className="text-sm text-gray-500">{transfer.description}</p>
                              )}
                            </div>
                            <p className="text-sm text-gray-500">
                              {new Date(transfer.created_at).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Send className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No transfers yet</h3>
                    <p className="text-gray-500 mb-4">Start by making your first money transfer</p>
                    <button
                      onClick={() => setShowTransferForm(true)}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Make a Transfer
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Other tabs can be implemented similarly */}
        {activeTab !== 'overview' && activeTab !== 'accounts' && activeTab !== 'transfers' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Coming Soon
            </h3>
            <p className="text-gray-600">
              This feature is under development. Please check back later.
            </p>
          </div>
        )}
      </main>

      {/* Enhanced Chatbot */}
      <Chatbot isOpen={showChatbot} onClose={() => setShowChatbot(false)} />

      {/* Transfer Form */}
      <TransferForm 
        isOpen={showTransferForm} 
        onClose={() => setShowTransferForm(false)}
        onSuccess={handleTransferSuccess}
      />
    </div>
  );
}