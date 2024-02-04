import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
# Добавление пути к папке с ботами в sys.path для доступа к модулям бота
sys.path.append(str(Path(__file__).parent.parent / 'bots'))
from bot_ru import echo, start  # noqa: E402


class TestBotRu(unittest.TestCase):
    def setUp(self):
        self.update = MagicMock()
        self.context = MagicMock()
        # Установка chat_id для мокированного объекта update.message
        self.update.message.chat_id = 1234
        # Мокирование метода reply_text внутри update.message
        self.update.message.reply_text = MagicMock()

    @patch('bot_ru.generate_response', return_value='Это тестовый ответ')
    def test_echo(self, mock_generate_response):
        # Имитация входящего сообщения
        self.update.message.text = "Привет"
        echo(self.update, self.context)
        # Проверка, что reply_text был вызван с ожидаемым ответом
        self.update.message.reply_text.assert_called_once_with('Это тестовый ответ')

    def test_start(self):
        start(self.update, self.context)
        # Проверка, что reply_text был вызван с ожидаемым приветствием
        self.update.message.reply_text.assert_called_once_with('Привет! Я ваш чат-бот.')


if __name__ == '__main__':
    unittest.main()
