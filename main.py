import requests
from telegram.ext import Application, CommandHandler

# Token của bạn
TELEGRAM_TOKEN = "8243360646:AAFdPeTuBeIeGbK03EctyTrfCK0-wlYKxSI"
HF_TOKEN = "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"

HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(prompt: str) -> str:
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except Exception:
            return str(response.json())
    else:
        return f"Lỗi HuggingFace: {response.status_code} - {response.text}"

async def start(update, context):
    await update.message.reply_text("🤖 Bot chạy trên Render thành công!\nDùng /ask <câu hỏi> để hỏi AI.")

async def ask(update, context):
    if not context.args:
        await update.message.reply_text("Bạn chưa nhập câu hỏi. Ví dụ: /ask Xin chào")
        return
    prompt = " ".join(context.args)
    await update.message.reply_text("⏳ Đang gọi HuggingFace API...")
    reply = query_hf(prompt)
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    app.run_polling()

if __name__ == "__main__":
    main()
