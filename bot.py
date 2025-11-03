# bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID
from scanner import scan_file
from database import init_db, log_scan

# Dastlab bazani tayyorlaymiz
init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n"
        "Men siz yuborgan faylni xavfsizlik uchun tekshiraman.\n"
        "📎 Iltimos, fayl yuboring."
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    user_id = update.message.from_user.id
    file_name = document.file_name
    file_path = f"downloads/{file_name}"

    os.makedirs("downloads", exist_ok=True)
    new_file = await document.get_file()
    await new_file.download_to_drive(file_path)

    await update.message.reply_text("🧠 Fayl tekshirilmoqda... Iltimos, kuting...")

    result = scan_file(file_path)
    os.remove(file_path)

    msg = (
        f"📄 **Fayl:** {file_name}\n"
        f"📦 **Turi:** {result['file_type']}\n"
        f"🧬 **Hash:** `{result['hash']}`\n"
        f"🛡 **Holat:** {result['virus_status']}"
    )

    if result['virustotal']:
        msg += f"\n\n🌐 {result['virustotal']}"

    await update.message.reply_text(msg, parse_mode="Markdown")

    log_scan(file_name, result['file_type'], result['hash'], result['virus_status'], user_id)

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ Sizda bu buyruq uchun ruxsat yo‘q.")
    import sqlite3
    conn = sqlite3.connect("logs/files.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*), status FROM scans GROUP BY status")
    stats = c.fetchall()
    conn.close()
    text = "📊 *Skanerlash statistikasi:*\n"
    for s in stats:
        text += f"{s[1]}: {s[0]} ta\n"
    await update.message.reply_text(text, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", admin_stats))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

if __name__ == "__main__":
    print("🤖 Universal File Guard ishga tushmoqda...")
    app.run_polling()
