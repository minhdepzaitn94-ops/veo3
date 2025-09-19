import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "ali-vilab/InstructVideo"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Gửi cho mình 1 ảnh, mình sẽ tạo video VEO3 từ ảnh đó!")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    img_path = "input.jpg"
    await file.download_to_drive(img_path)

    await update.message.reply_text("⏳ Đang tạo video, vui lòng chờ...")

    with open(img_path, "rb") as f:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_ID}",
            headers=headers,
            data=f
        )

    if response.status_code != 200:
        await update.message.reply_text("❌ Lỗi API HuggingFace, thử lại sau!")
        return

    out_path = "output.mp4"
    with open(out_path, "wb") as f:
        f.write(response.content)

    await update.message.reply_video(video=open(out_path, "rb"))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    print("✅ Bot đang chạy trên Railway...")
    app.run_polling()

if __name__ == "__main__":
    main()
