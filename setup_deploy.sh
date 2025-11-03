#!/bin/bash

echo "🚀 Universal File Guard deploy setup boshlanmoqda..."

# 1️⃣ GitHub foydalanuvchi nomi va tokenini so‘rash
read -p "GitHub foydalanuvchi nomi (username): " GH_USER
read -p "Yangi repo nomi (masalan: universal_file_guard): " GH_REPO
read -p "GitHub Personal Access Token (PAT): " GH_TOKEN

# 2️⃣ Git init qilish
cd ~/universal_file_guard || { echo "❌ Papka topilmadi!"; exit 1; }
git init
git add .
git commit -m "Initial commit"
git branch -M main

# 3️⃣ GitHub’da repo yaratish (API orqali)
echo "🌐 GitHub’da yangi repo yaratilmoqda..."
curl -u "$GH_USER:$GH_TOKEN" https://api.github.com/user/repos -d "{\"name\":\"$GH_REPO\"}"

# 4️⃣ Ulanish va push qilish
git remote add origin https://github.com/$GH_USER/$GH_REPO.git
git push -u origin main

echo "✅ GitHub repo tayyor: https://github.com/$GH_USER/$GH_REPO"

# 5️⃣ Render deploy bo‘yicha eslatma
echo ""
echo "📋 Endi https://render.com saytiga kiring."
echo "👉 'New Web Service' tanlang"
echo "👉 GitHub ulanadi va '$GH_REPO' repongizni tanlang"
echo ""
echo "⚙️ Build Command: pip install -r requirements.txt"
echo "⚙️ Start Command: python bot.py"
echo ""
echo "🔑 Environment Variables kiriting:"
echo "   BOT_TOKEN=(sizning bot tokeningiz)"
echo "   VT_API_KEY=(VirusTotal API key)"
echo ""
echo "✅ Keyin 'Deploy Web Service' bosib tugating!"
