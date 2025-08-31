# 🚀 BankBot Quick Start Guide

Get BankBot up and running in minutes!

## ⚡ Quick Start (5 minutes)

### 1. Start the Backend
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### 2. Start the Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin

### 4. Login with Demo Accounts
- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`

## 🎯 What You Can Do

### Banking Portal
- ✅ View account balances
- ✅ Check transaction history
- ✅ Transfer money between accounts
- ✅ Manage user profile

### AI Chatbot
- ✅ Ask banking questions naturally
- ✅ Check balances via chat
- ✅ Get transaction information
- ✅ Learn about banking services

## 🔧 Troubleshooting

### Backend Issues
```bash
# Check if Django is running
curl http://localhost:8000/admin/

# Restart Django
cd backend
source venv/bin/activate
python manage.py runserver
```

### Frontend Issues
```bash
# Check if Next.js is running
curl http://localhost:3000

# Restart Next.js
cd frontend
npm run dev
```

### Database Issues
```bash
cd backend
source venv/bin/activate
python manage.py migrate
python manage.py populate_data
python manage.py populate_faqs
```

## 🚀 Production Deployment

### Backend
1. Set `DEBUG=False` in settings
2. Use PostgreSQL instead of SQLite
3. Configure environment variables
4. Use Gunicorn + Nginx

### Frontend
1. Build: `npm run build`
2. Deploy to Vercel/Netlify
3. Set API endpoint environment variables

## 📚 Learn More

- **Full Documentation**: README.md
- **API Reference**: Check the API endpoints in the code
- **Admin Panel**: http://localhost:8000/admin (admin/admin123)

---

**Need help?** Check the main README.md or create an issue! 🆘