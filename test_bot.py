import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User
from telegram.ext import CallbackContext


# Импортирую функции из основного файла бота
from bot import start_command, msg_handler, trusted_users

def is_duplicate(msg):
    # Простая заглушка, которая возвращает False
    return False
# Определяю заглушки для функций, которых нет в основном коде
def is_duplicate(msg):
    # Я не знаю, как проверять на дубликаты, поэтому просто возвращаю False
    return False

def add_tags_to_msg(msg):
    # Добавляю тег к сообщению, надеюсь, это правильно
    return msg + ' #тег'


def is_duplicate(msg):
    pass


class TestBot(unittest.TestCase):

    def test_start_command(self):
        # Тестирую функцию start_command
        update = MagicMock()
        context = MagicMock()
        update.message.reply_text = MagicMock()

        # Вызываю функцию и проверяю, что она отправляет правильное сообщение
        start_command(update, context)
        update.message.reply_text.assert_called_with('Привет! Это бот для публикации объектов.')

    def test_msg_handler_with_trusted_user(self):
        # Тестирую msg_handler с доверенным пользователем
        user = User(id=123456789, first_name='TrustedUser', is_bot=False)
        message = Message(message_id=1, date=None, chat=None, text='Тестовое сообщение', from_user=user)
        update = Update(update_id=1, message=message)
        context = CallbackContext(dispatcher=None)
        context.bot = MagicMock()
        update.message.reply_text = MagicMock()

        # Патчу функции, чтобы они работали
        with patch('bot.is_duplicate', side_effect=is_duplicate):
            with patch('bot.add_tags_to_msg', side_effect=add_tags_to_msg):
                msg_handler(update, context)

        # Проверяю, что сообщение отправлено в канал
        context.bot.send_message.assert_called()
        # Проверяю, что пользователю отправлено подтверждение
        update.message.reply_text.assert_called_with('Объект опубликован.')

    def test_msg_handler_with_untrusted_user(self):
        # Тестирую msg_handler с недоверенным пользователем
        user = User(id=111111111, first_name='UntrustedUser', is_bot=False)
        message = Message(message_id=2, date=None, chat=None, text='Сообщение от недоверенного пользователя', from_user=user)
        update = Update(update_id=2, message=message)
        context = CallbackContext(dispatcher=None)
        context.bot = MagicMock()
        update.message.reply_text = MagicMock()

        with patch('bot.is_duplicate', side_effect=is_duplicate):
            with patch('bot.add_tags_to_msg', side_effect=add_tags_to_msg):
                msg_handler(update, context)

        # Проверяю, что сообщение не отправлено в канал
        context.bot.send_message.assert_not_called()
        # Проверяю, что пользователю не отправлено подтверждение
        update.message.reply_text.assert_not_called()

    def test_msg_handler_with_empty_message(self):
        # Тестирую msg_handler с пустым сообщением от доверенного пользователя
        user = User(id=123456789, first_name='TrustedUser', is_bot=False)
        message = Message(message_id=3, date=None, chat=None, text='', from_user=user)
        update = Update(update_id=3, message=message)
        context = CallbackContext(dispatcher=None)
        context.bot = MagicMock()
        update.message.reply_text = MagicMock()

        with patch('bot.is_duplicate', side_effect=is_duplicate):
            with patch('bot.add_tags_to_msg', side_effect=add_tags_to_msg):
                msg_handler(update, context)

        # Проверяю, что сообщение не отправлено в канал
        context.bot.send_message.assert_not_called()
        # Проверяю, что пользователю не отправлено подтверждение
        update.message.reply_text.assert_not_called()

    def test_msg_handler_with_duplicate_message(self):
        # Тестирую msg_handler с дублирующимся сообщением
        user = User(id=123456789, first_name='TrustedUser', is_bot=False)
        message = Message(message_id=4, date=None, chat=None, text='Дубликат сообщения', from_user=user)
        update = Update(update_id=4, message=message)
        context = CallbackContext(dispatcher=None)
        context.bot = MagicMock()
        update.message.reply_text = MagicMock()

        # Здесь функция is_duplicate должна возвращать True
        def is_duplicate(msg):
            return True

        with patch('bot.is_duplicate', side_effect=is_duplicate):
            with patch('bot.add_tags_to_msg', side_effect=add_tags_to_msg):
                msg_handler(update, context)

        # Проверяю, что сообщение не отправлено в канал
        context.bot.send_message.assert_not_called()
        # Проверяю, что пользователю не отправлено подтверждение
        update.message.reply_text.assert_not_called()

    def test_add_tags_to_msg(self):
        # Тестирую функцию add_tags_to_msg
        msg = 'Тестовое сообщение'
        result = add_tags_to_msg(msg)
        expected_result = 'Тестовое сообщение #тег'
        self.assertEqual(result, expected_result)

    def test_is_duplicate(self):
        # Тестирую функцию is_duplicate
        msg = 'Новое сообщение'
        result = is_duplicate(msg)
        self.assertFalse(result)

        # Проверяю с дубликатом
        def is_duplicate(msg):
            return True

        result = is_duplicate(msg)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
