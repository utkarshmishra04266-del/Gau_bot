import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import csv, random
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6380152779
PASSKEY = "GAO MATA KI JAI"
unlocked = set()

def save_report(rid, uid, username, rtype, text):
    file_exists = os.path.isfile('reports.csv')
    with open('reports.csv', 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(['ReportID', 'Date', 'UserID', 'Username', 'Type', 'Text'])
        w.writerow([rid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), uid, username, rtype, text])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Jai Gau Mata! 🙏\nPasskey bhejo: GAO MATA KI JAI")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (update.message.text or "").strip()
    uid = update.effective_user.id
    username = update.effective_user.username or "NoUsername"
    if txt.upper() == PASSKEY:
        unlocked.add(uid)
        await update.message.reply_text("✅ Unlocked! Ab report bhejo")
        return
    if uid not in unlocked:
        await update.message.reply_text("❌ Pehle passkey bhejo")
        return
    report_id = random.randint(1000, 9999)
    rtype = "TEXT"
    if update.message.photo: rtype = "PHOTO"
    elif update.message.video: rtype = "VIDEO"
    save_report(report_id, uid, username, rtype, txt)
    caption = f"🚨 NEW REPORT #{report_id}\nFrom: @{username} ({uid})\nType: {rtype}\nDetails: {txt}"
    try:
        if update.message.photo:
            await context.bot.send_photo(ADMIN_ID, photo=update.message.photo[-1].file_id, caption=caption)
        elif update.message.video:
            await context.bot.send_video(ADMIN_ID, video=update.message.video.file_id, caption=caption)
        else:
            await context.bot.send_message(ADMIN_ID, caption)
    except: pass
    await update.message.reply_text(f"✅ Report save ID: #{report_id}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle))
app.run_polling()
