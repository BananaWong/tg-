from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters
import os

app = Flask(__name__)
TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# 特定關鍵詞列表
KEYWORDS = ['愿意叫妈妈的来', '送福利群三个','小项目政策下研发项目','猎奇血腥类及新增人兽类','最新黑科技打法招人合作','找几个帮手干活一天做四个钟','年度暴润项目','上浮收U','想搞钱的可以联系我','全网最高赔率','2.8玩法公平公正公开']

def handle_message(update, context):
    message = update.message
    for keyword in KEYWORDS:
        if keyword in message.text:
            chat_id = message.chat_id
            user_id = message.from_user.id
            message_id = message.message_id

            # 刪除消息
            context.bot.delete_message(chat_id=chat_id, message_id=message_id)

            # 踢出發送者
            context.bot.kick_chat_member(chat_id=chat_id, user_id=user_id)
            break

# 添加消息處理器
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route('/' + TOKEN, methods=['POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == "__main__":
    app.run(threaded=True)
