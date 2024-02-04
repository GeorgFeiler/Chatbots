from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from transformers import GPT2LMHeadModel, GPT2Tokenizer

chatbot_model = "sberbank-ai/rugpt3small_based_on_gpt2"

token = "Введите здесь API Token вашего Telegram-бота"


# Настройка модели GPT-3 на русском языке
def setup_gpt3_model(model_name=chatbot_model):
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    return model, tokenizer


# Генерация ответа
def generate_response(question, model, tokenizer):
    input_ids = tokenizer.encode(question, return_tensors='pt')
    output = model.generate(input_ids,
                            max_length=100,
                            num_return_sequences=1,
                            no_repeat_ngram_size=2,
                            early_stopping=True,
                            temperature=0.7,
                            top_k=50,
                            top_p=0.9)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    response = response.replace(question, "").strip()
    return response


# Инициализация модели GPT-3 на русском языке
gpt3_model, gpt3_tokenizer = setup_gpt3_model()


def start(update, context):
    update.message.reply_text('Привет! Я ваш чат-бот.')


def echo(update, context):
    question = update.message.text
    answer = generate_response(question, gpt3_model, gpt3_tokenizer)
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
