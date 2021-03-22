from telegram.ext import Updater
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater = Updater(token='1723327297:AAGDyTGu9M8iQE_VGxX9J-PpVmP33xgchZI', use_context=True)
dispatcher = updater.dispatcher
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="你好!\n你的chatid是："+str(update.effective_chat.id))

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()





























character = [0, "🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏"]
bamboo = [0, "🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"]
bamboo = [0, "🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"]
dot = [0, "🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡"]
wind = [0, "🀀", "🀁", "🀂", "🀃"]
dragon = [0, "🀄", "🀅", "🀆"]
alltile = [character, bamboo, dot, wind, dragon]


def tomahjong(id):
    if(isinstance(id, int)): return alltile[int(id/10)][id % 10]
    else: return list(map(tomahjong, id))
#print(tomahjong(22))