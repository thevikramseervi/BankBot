# BankBot – AI Chatbot for Banking FAQs

A full-stack web application featuring a modern banking portal with an AI-powered chatbot that understands natural language queries and provides banking assistance.

## 🚀 Features

### Banking Portal
- **User Authentication**: Secure login/registration system
- **Account Management**: View account balances and details
- **Transaction History**: Track all banking transactions
- **Money Transfers**: Transfer funds between accounts
- **Real-time Updates**: Live balance and transaction updates

### AI Chatbot (BankBot)
- **Natural Language Understanding**: Powered by scikit-learn and NLTK
- **Intent Detection**: Automatically identifies user intentions
- **Entity Extraction**: Extracts amounts, account numbers, dates
- **Contextual Responses**: Provides relevant banking information
- **Training Capabilities**: Can be trained with new FAQ data

### Technology Stack
- **Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **Backend**: Django 5.2 with Django REST Framework
- **AI/ML**: scikit-learn, NLTK, TF-IDF vectorization
- **Database**: SQLite (can be easily migrated to PostgreSQL/MySQL)
- **Authentication**: Django session-based authentication

## 🏗️ Project Structure

```
bankbot-app/
├── backend/                 # Django backend
│   ├── banking/            # Banking app models and views
│   ├── chatbot/            # Chatbot app with NLU
│   ├── bankbot_project/    # Django project settings
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   └── components/    # React components
│   ├── package.json       # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS configuration
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd bankbot-app/backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Populate initial data:**
   ```bash
   python manage.py populate_data
   python manage.py populate_faqs
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd bankbot-app/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## 🧪 Demo Accounts

The system comes with pre-configured demo accounts:

- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`

## 🔧 API Endpoints

### Banking API (`/api/banking/`)
- `GET /accounts/` - List user accounts
- `GET /accounts/{id}/transactions/` - Get account transactions
- `GET /transactions/` - List user transactions
- `POST /transfers/` - Create money transfer
- `GET /stats/summary/` - Get banking summary

### Chatbot API (`/api/chatbot/`)
- `POST /chat/chat/` - Send message to chatbot
- `GET /faqs/` - List FAQ entries
- `POST /chat/train/` - Train chatbot with new data
- `GET /intents/` - List available intents

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

## 🤖 Chatbot Capabilities

The AI chatbot can understand and respond to:

- **Balance Inquiries**: "What's my balance?" "How much money do I have?"
- **Transfer Requests**: "I want to transfer $500 to account 1234-5678-9012-3456"
- **Transaction History**: "Show me my recent transactions"
- **Account Information**: "Tell me about my accounts"
- **General Help**: "How do I reset my password?"

### Training the Chatbot

You can train the chatbot with new data using the management command:

```bash
python manage.py populate_faqs
```

Or through the API:

```bash
curl -X POST http://localhost:8000/api/chatbot/chat/train/ \
  -H "Content-Type: application/json" \
  -d '{
    "questions": ["How do I open a new account?"],
    "answers": ["You can open a new account by visiting any branch or calling our customer service."],
    "intent": "open_account",
    "category": "account_management"
  }'
```

## 🔒 Security Features

- **Session-based Authentication**: Secure user sessions
- **CSRF Protection**: Built-in Django CSRF protection
- **Input Validation**: Comprehensive form and API validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Content Security Policy headers

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG=False` in settings
2. Configure production database (PostgreSQL recommended)
3. Set secure `SECRET_KEY`
4. Configure `ALLOWED_HOSTS`
5. Use production WSGI server (Gunicorn + Nginx)

### Frontend Deployment
1. Build production version: `npm run build`
2. Deploy to Vercel, Netlify, or any static hosting
3. Configure environment variables for API endpoints

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📊 Monitoring & Analytics

- **Django Admin**: Built-in admin interface at `/admin/`
- **Database Logging**: Transaction and user activity logs
- **Chatbot Analytics**: Intent detection accuracy and usage statistics

## 🔮 Future Enhancements

- **Multi-language Support**: Internationalization for global users
- **Voice Integration**: Speech-to-text and text-to-speech
- **Advanced Analytics**: Machine learning insights and predictions
- **Mobile App**: React Native mobile application
- **Blockchain Integration**: Cryptocurrency support
- **Advanced Security**: Biometric authentication, 2FA

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the Django and Next.js documentation
- Review the API documentation above

## 🙏 Acknowledgments

- Django team for the excellent web framework
- Next.js team for the React framework
- scikit-learn and NLTK communities for ML/NLP tools
- Tailwind CSS for the utility-first CSS framework

---

**BankBot** - Making banking smarter, one conversation at a time! 🏦✨