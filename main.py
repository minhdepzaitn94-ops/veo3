import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ====== TOKEN ======
TELEGRAM_TOKEN = "8230953173:AAHiCH_iJWZTxatCI3_Jba4kT90I6F1U--o"
HF_TOKEN = "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"
HF_API_URL = "https://api-inference.huggingface.co/models/ntt123/vietTTS_fpt"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# ----- Lệnh /speak -----
async def speak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Vui lòng nhập văn bản. Ví dụ: /speak Xin chào bạn!")
        return

    text = " ".join(context.args)
    await update.message.reply_text("⏳ Đang tạo giọng nói...")

    voice_file = generate_tts(text)
    if voice_file:
        await update.message.reply_voice(voice=open(voice_file, "rb"))
    else:
        await update.message.reply_text("⚠️ Lỗi khi tạo giọng nói!")

# ----- Hàm gọi API TTS -----
def generate_tts(text: str, filename="voice_part.mp3"):
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": text})
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        print("Error:", response.text)
        return None

# ----- Xử lý file txt/srt -----
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = "input.txt"
    await file.download_to_drive(file_path)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    await update.message.reply_text("⏳ Đang chuyển văn bản trong file thành giọng nói...")

    # Chia nhỏ text nếu quá dài
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    output_files = []

    for idx, chunk in enumerate(chunks):
        voice_file = generate_tts(chunk, f"voice_{idx}.mp3")
        if voice_file:
            output_files.append(voice_file)

    if output_files:
        if len(output_files) == 1:
            await update.message.reply_voice(voice=open(output_files[0], "rb"))
        else:
            final_file = "final_voice.mp3"
            with open(final_file, "wb") as outfile:
                for fname in output_files:
                    with open(fname, "rb") as infile:
                        outfile.write(infile.read())
            await update.message.reply_document(document=open(final_file, "rb"), filename="output.mp3")
    else:
        await update.message.reply_text("⚠️ Không tạo được giọng nói!")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("speak", speak))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("🚀 Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
