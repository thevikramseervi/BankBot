'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Eye, EyeOff, Lock, User, Building2, MessageCircle, 
  Shield, CreditCard, TrendingUp, Globe, ArrowRight,
  CheckCircle, Star, Zap
} from 'lucide-react';

export default function Home() {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    confirmPassword: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [currentFeature, setCurrentFeature] = useState(0);
  const router = useRouter();

  // Auto-rotate features
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % 3);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: <MessageCircle className="h-8 w-8" />,
      title: "AI-Powered Banking",
      description: "Get instant answers and perform transactions through natural conversation with our intelligent BankBot."
    },
    {
      icon: <Shield className="h-8 w-8" />,
      title: "Bank-Grade Security",
      description: "Your data is protected with enterprise-level encryption and multi-factor authentication."
    },
    {
      icon: <TrendingUp className="h-8 w-8" />,
      title: "Smart Insights",
      description: "Get personalized financial insights and recommendations to optimize your banking experience."
    }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (isLogin) {
        const response = await fetch('http://localhost:8000/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            username: formData.username,
            password: formData.password,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Login successful:', data);
          router.push('/dashboard');
        } else {
          const errorData = await response.json();
          alert(`Login failed: ${errorData.error || 'Please check your credentials.'}`);
        }
      } else {
        if (formData.password !== formData.confirmPassword) {
          alert('Passwords do not match');
          return;
        }

        const response = await fetch('http://localhost:8000/api/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: formData.username,
            email: formData.email,
            password: formData.password,
          }),
        });

        if (response.ok) {
          alert('Registration successful! Please log in.');
          setIsLogin(true);
        } else {
          const errorData = await response.json();
          alert(`Registration failed: ${errorData.error || 'Please try again.'}`);
        }
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20" />
        <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob" />
        <div className="absolute top-0 -right-4 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000" />
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000" />
      </div>

      {/* Header */}
      <header className="relative z-10 bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
                <Building2 className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                BankBot
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-blue-200 font-medium">AI-Powered Banking</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left Side - Features */}
          <div className="space-y-8">
            <div>
              <h2 className="text-5xl font-bold text-white mb-6 leading-tight">
                Welcome to the
                <span className="block bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Future of Banking
                </span>
              </h2>
              <p className="text-xl text-blue-100 mb-8 leading-relaxed">
                Experience seamless banking with our AI-powered chatbot that understands your needs and provides instant assistance.
              </p>
            </div>

            {/* Animated Feature Cards */}
            <div className="space-y-6">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className={`flex items-start space-x-4 p-4 rounded-2xl transition-all duration-500 ${
                    currentFeature === index
                      ? 'bg-white/20 backdrop-blur-md border border-white/30 scale-105'
                      : 'bg-white/10 backdrop-blur-md border border-white/20'
                  }`}
                >
                  <div className={`flex-shrink-0 p-3 rounded-xl transition-all duration-300 ${
                    currentFeature === index
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                      : 'bg-white/20 text-blue-200'
                  }`}>
                    {feature.icon}
                  </div>
                  <div>
                    <h3 className={`text-lg font-semibold transition-colors duration-300 ${
                      currentFeature === index ? 'text-white' : 'text-blue-100'
                    }`}>
                      {feature.title}
                    </h3>
                    <p className={`text-sm transition-colors duration-300 ${
                      currentFeature === index ? 'text-blue-100' : 'text-blue-200'
                    }`}>
                      {feature.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-white">99.9%</div>
                <div className="text-sm text-blue-200">Uptime</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-white">24/7</div>
                <div className="text-sm text-blue-200">Support</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-white">256-bit</div>
                <div className="text-sm text-blue-200">Encryption</div>
              </div>
            </div>
          </div>

          {/* Right Side - Login/Register Form */}
          <div className="bg-white/10 backdrop-blur-xl rounded-3xl border border-white/20 shadow-2xl p-8">
            <div className="text-center mb-8">
              <h3 className="text-3xl font-bold text-white mb-2">
                {isLogin ? 'Welcome Back' : 'Create Account'}
              </h3>
              <p className="text-blue-200">
                {isLogin ? 'Sign in to your account' : 'Join BankBot today'}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-blue-100 mb-2">
                  Username
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-blue-300" />
                  </div>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleInputChange}
                    required
                    className="block w-full pl-10 pr-3 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-blue-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                    placeholder="Enter your username"
                  />
                </div>
              </div>

              {!isLogin && (
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-blue-100 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="block w-full px-3 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-blue-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                    placeholder="Enter your email"
                  />
                </div>
              )}

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-blue-100 mb-2">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-blue-300" />
                  </div>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                    className="block w-full pl-10 pr-12 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-blue-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                    placeholder="Enter your password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-blue-300 hover:text-white transition-colors"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </div>

              {!isLogin && (
                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-blue-100 mb-2">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required
                    className="block w-full px-3 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-blue-200 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                    placeholder="Confirm your password"
                  />
                </div>
              )}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 font-semibold text-lg"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Loading...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-2">
                    <span>{isLogin ? 'Sign In' : 'Create Account'}</span>
                    <ArrowRight className="h-5 w-5" />
                  </div>
                )}
              </button>
            </form>

            <div className="mt-6 text-center">
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-blue-300 hover:text-white font-medium transition-colors"
              >
                {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
              </button>
            </div>

            {isLogin && (
              <div className="mt-6 p-4 bg-white/10 rounded-xl border border-white/20">
                <h4 className="text-sm font-medium text-white mb-3 flex items-center">
                  <Star className="h-4 w-4 mr-2 text-yellow-400" />
                  Demo Accounts
                </h4>
                <div className="text-sm text-blue-200 space-y-2">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-400" />
                    <span>Username: <span className="font-mono text-white">john_doe</span></span>
                    <span>Password: <span className="font-mono text-white">password123</span></span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-400" />
                    <span>Username: <span className="font-mono text-white">jane_smith</span></span>
                    <span>Password: <span className="font-mono text-white">password123</span></span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
