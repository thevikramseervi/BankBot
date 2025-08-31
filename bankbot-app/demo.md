# 🎯 BankBot Demo Guide

Welcome to BankBot! This guide will walk you through testing all the features of our AI-powered banking application.

## 🚀 Quick Demo Setup

### 1. Start Both Servers
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 2. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin

## 🧪 Demo Walkthrough

### Step 1: Landing Page
1. Open http://localhost:3000
2. You'll see the beautiful landing page with:
   - BankBot branding and features
   - Login/Register form
   - Demo account information

### Step 2: Login with Demo Accounts
Use one of these pre-configured accounts:
- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`

### Step 3: Explore the Dashboard

#### 📊 Overview Tab
- **Total Balance**: Shows combined balance across all accounts
- **Active Accounts**: Number of active banking accounts
- **Pending Transfers**: Any transfers in progress
- **Recent Transactions**: Last 10 banking transactions

#### 🏦 Accounts Tab
- **Checking Account**: Primary account for daily transactions
- **Savings Account**: Interest-earning account
- **Account Details**: Account numbers, types, and balances

#### 💰 Transfers Tab
- **View Transfers**: See all your transfer history
- **New Transfer**: Click "New Transfer" button
- **Transfer Form**: Enter destination account, amount, and description
- **Real-time Processing**: Transfers are processed immediately

#### 🔍 Transactions Tab
- **Transaction History**: Complete list of all transactions
- **Transaction Types**: Deposits, withdrawals, transfers, payments
- **Reference Numbers**: Unique identifiers for each transaction

### Step 4: Test the AI Chatbot

#### 🎯 Open Chatbot
1. Click "Chat with BankBot" button in the header
2. A beautiful chat interface will appear

#### 🤖 Test Natural Language Queries
Try these example questions:

**Balance Inquiries:**
- "What's my current balance?"
- "How much money do I have?"
- "Show me my account balance"

**Transfer Requests:**
- "I want to transfer $100 to account 1234-5678-9012-3456"
- "Transfer $50 to my savings account"
- "Send $200 to account 1111-2222-3333-4444"

**Transaction Information:**
- "Show my recent transactions"
- "What transactions did I make yesterday?"
- "Tell me about my account activity"

**General Banking:**
- "What are your banking hours?"
- "How do I reset my password?"
- "What fees do you charge?"

#### 🔍 Observe AI Responses
The chatbot will:
- **Detect Intent**: Show what it understood (e.g., "check_balance")
- **Extract Entities**: Identify amounts, account numbers, dates
- **Provide Contextual Responses**: Give relevant banking information
- **Show Confidence**: Display how sure it is about the intent

### Step 5: Test Money Transfers

#### 💸 Create a Transfer
1. Go to Transfers tab
2. Click "New Transfer"
3. Enter destination account: `1111-2222-3333-4444` (Jane's account)
4. Enter amount: `100.00`
5. Add description: "Demo transfer"
6. Click "Send Transfer"

#### ✅ Verify Transfer
1. Check the transfer appears in your transfers list
2. Verify account balances are updated
3. Check transaction history for the transfer

### Step 6: Explore Admin Panel

#### 🔧 Access Admin
1. Go to http://localhost:8000/admin
2. Login with: `admin` / `admin123`

#### 📊 View Data
- **Users**: See demo users and their profiles
- **Accounts**: View all banking accounts
- **Transactions**: Browse transaction history
- **Transfers**: Monitor money transfers
- **Chatbot Data**: View FAQs, intents, and conversations

## 🎭 Demo Scenarios

### Scenario 1: New User Experience
1. Register a new account
2. Login and explore the dashboard
3. Ask BankBot basic questions
4. Make your first transfer

### Scenario 2: Power User Experience
1. Login with existing account
2. Check multiple account balances
3. Review transaction history
4. Make several transfers
5. Have complex conversations with BankBot

### Scenario 3: AI Training Demo
1. Go to admin panel
2. Add new FAQ entries
3. Test chatbot with new questions
4. Observe improved responses

## 🔍 Testing Checklist

- [ ] ✅ Landing page loads correctly
- [ ] ✅ Login/Register functionality works
- [ ] ✅ Dashboard displays account information
- [ ] ✅ All tabs are functional
- [ ] ✅ Chatbot opens and responds
- [ ] ✅ Natural language queries work
- [ ] ✅ Transfer form functions properly
- [ ] ✅ Real-time balance updates
- [ ] ✅ Transaction history displays
- [ ] ✅ Admin panel accessible
- [ ] ✅ Data persistence works

## 🐛 Troubleshooting

### Common Issues

**Backend Not Starting:**
```bash
cd backend
source venv/bin/activate
python manage.py migrate
python manage.py populate_data
python manage.py populate_faqs
python manage.py runserver
```

**Frontend Not Loading:**
```bash
cd frontend
npm install
npm run dev
```

**Database Issues:**
```bash
cd backend
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

**Chatbot Not Responding:**
- Check backend is running
- Verify API endpoints are accessible
- Check browser console for errors

## 🎉 Demo Success Indicators

You'll know the demo is successful when:

1. **User can login** with demo credentials
2. **Dashboard shows real data** (balances, transactions)
3. **Chatbot responds intelligently** to banking questions
4. **Transfers process successfully** and update balances
5. **All UI components** are responsive and beautiful
6. **Admin panel** shows comprehensive data management

## 🚀 Next Steps

After the demo, users can:

1. **Explore the codebase** to understand the architecture
2. **Customize the chatbot** with new training data
3. **Add new banking features** like bill payments
4. **Deploy to production** with proper security
5. **Scale the AI model** with more training data

---

**🎯 Demo Goal**: Showcase a production-ready banking application with AI chatbot capabilities that rivals commercial banking platforms!

**💡 Pro Tip**: Have the demo accounts ready and test all features before presenting to ensure a smooth experience.