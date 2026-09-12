import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6380152779

def start(update: Update, context: CallbackContext):
    update.message.reply_text("GAU MATA KI JAI 🙏\nAb aap photo/video/text bhejo, report ban jayegi.")

def handle_all(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = f"🚨 New Report\nFrom: {user.first_name} (@{user.username})\nID: {user.id}\n\n"
    
    if update.message.text:
        msg += f"Text: {update.message.text}"
        context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    elif update.message.photo:
        msg += "Type: Photo"
        context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    elif update.message.video:
        msg += "Type: Video"
        context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    else:
        context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)

    update.message.reply_text("✅ Report bhej di gayi hai. Gau Mata ki Jai!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, handle_all))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()    elif update.message.video: rtype = "VIDEO"
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
