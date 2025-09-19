import requests
from telegram.ext import Updater, CommandHandler

# Token đã nhúng sẵn
TELEGRAM_TOKEN = "8243360646:AAFdPeTuBeIeGbK03EctyTrfCK0-wlYKxSI"
HF_TOKEN = "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"

# API HuggingFace mẫu (bạn có thể đổi sang model khác)
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(prompt):
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        try:
            return data[0]["generated_text"]
        except:
            return str(data)
    else:
        return f"Lỗi HuggingFace: {response.status_code} - {response.text}"

def start(update, context):
    update.message.reply_text("🤖 Bot đã hoạt động trên Render!\nDùng /ask <câu hỏi> để hỏi AI.")

def ask(update, context):
    if not context.args:
        update.message.reply_text("Vui lòng nhập câu hỏi. Ví dụ: /ask Xin chào")
        return
    prompt = " ".join(context.args)
    update.message.reply_text("⏳ Đang gọi HuggingFace API...")
    reply = query_hf(prompt)
    update.message.reply_text(reply)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ask", ask))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
