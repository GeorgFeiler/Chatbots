from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

chatbot_model = "facebook/blenderbot-400M-distill"

token = "Введите здесь API Token вашего Telegram-бота"

# Настройка модели
def setup_blenderbot_model(model_name=chatbot_model):
    tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
    return model, tokenizer

# Генерация ответа
def generate_response(question, model, tokenizer):
    inputs = tokenizer([question], return_tensors='pt')
    output = model.generate(**inputs, 
                            max_length=100, 
                            num_return_sequences=1,
                            no_repeat_ngram_size=2,
                            early_stopping=True,
                            temperature=0.7,
                            top_k=50,
                            top_p=0.9)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Инициализация модели
blenderbot_model, blenderbot_tokenizer = setup_blenderbot_model()

def start(update, context):
    update.message.reply_text('Hi! I am your chat-bot :)')

def echo(update, context):
    question = update.message.text
    answer = generate_response(question, blenderbot_model, blenderbot_tokenizer)
    update.message.reply_text(answer)

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
