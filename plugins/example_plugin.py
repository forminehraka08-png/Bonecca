class Plugin:
    help_text = "Дополнительная строка для команды /help: Пример-плагин!"

    def __init__(self, storage):
        self.storage = storage

    async def on_message(self, message, storage):
        # Пример обработки входящих сообщений
        if message.text and "плагин" in message.text.lower():
            await message.reply("Вас приветствует пример-плагин!")