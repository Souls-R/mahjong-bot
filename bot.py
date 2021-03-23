from telegram.ext import Updater
import telegram
import logging
from uuid import uuid4
import json
from telegram.ext import CommandHandler
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
#persistentdata = PicklePersistence(filename='userdata')
#updater = Updater(token='1723327297:AAGDyTGu9M8iQE_VGxX9J-PpVmP33xgchZI',persistence=persistentdata,use_context=True,request_kwargs={'proxy_url': 'http://127.0.0.1:7890/'})
updater = Updater(token='1723327297:AAGDyTGu9M8iQE_VGxX9J-PpVmP33xgchZI',use_context=True,request_kwargs={'proxy_url': 'http://127.0.0.1:7890/'})
dispatcher = updater.dispatcher

def start(update, context):
    context.user_data["id"] = update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="你好!\n你的chatid是："+str(update.effective_chat.id))

def play(update,context):
    player=Player(context,"a",update.effective_chat.id,0)
    board.add(player)

def confirm(context, messages):
    id=context.user_data.get("id")
    context.bot.send_message(id,text=str(id)+" :\n"+messages)
    return "多轮"

def setname(update, context):
    value = update.message.text.partition(' ')[2]
    context.user_data["name"] = value
    update.message.reply_text("昵称修改为："+value)

def getname(update, context):
    value = context.user_data.get("name", 'Not found')
    update.message.reply_text(value)


dispatcher.add_handler(CommandHandler('setname', setname))
dispatcher.add_handler(CommandHandler('getname', getname))
dispatcher.add_handler(CommandHandler('play', play))
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
    if(isinstance(id, int)):
        return alltile[int(id/10)][id % 10]
    else:
        return list(map(tomahjong, id))
