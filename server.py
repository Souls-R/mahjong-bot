from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, run_async
import time
import threading
from telegram.ext import Updater
import random
import json
# 🀀🀁🀂🀃🀄🀅🀆🀇🀈🀉🀊🀋🀌🀍🀎🀏🀐🀑🀒🀓🀔🀕🀖🀗🀘🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣🀤🀥🀦🀧🀨🀩🀪 🀫
alltileid = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             31, 32, 33, 34, 31, 32, 33, 34, 31, 32, 33, 34, 31, 32, 33, 34,
             41, 42, 43, 41, 42, 43, 41, 42, 43, 41, 42, 43]
character = [0, "🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏"]
bamboo = [0, "🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"]
dot = [0, "🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡"]
wind = [0, "🀀", "🀁", "🀂", "🀃"]
dragon = [0, "🀄", "🀅", "🀆"]
alltile = [character, bamboo, dot, wind, dragon]
"""
01-09 : 万子
11-19 : 条子
21-29 : 筒子
31-34 : 风牌
41-43 : 三元
"""


def tomahjong(id):
    # 将麻将id或id列表转换为emoji
    if(isinstance(id, int)):
        return alltile[int(id/10)][id % 10]
    else:
        return " ".join(list(map(tomahjong, id)))


def printjson(obj):
    # 将对象json序列化输出
    print(obj)
    # print(json.dumps(obj))


def runasync(func):
    #异步装饰器
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
        thr.setName("func{}".format(func.__name__))
        # thr.join()
        #print("ident={},\nname={},\enumerate={},\nactive={},\nalive={}".format(
        #    thr.ident, thr.getName(), threading.enumerate(), threading.active_count(), thr.is_alive))
        print("新线程添加：{}".format(func.__name__))
    return wrapper


def win(tiles):
    # 接受14张已排序的牌 返回是否胡牌
    if(len(tiles) == 14):
        for i in range(len(tiles)-1):
            if(tiles[i] == tiles[i+1]):
                temp = list(tiles)
                del temp[i:i+2]
                if(win(temp)):
                    return True
        return False

    if(len(tiles) == 2):
        if(tiles[0] == tiles[1]):
            return True

    if(len(tiles) <= 12):
        if(len(tiles) == 0):
            return True
        for i in tiles:
            if(tiles.count(i) >= 3):
                tiles.remove(i)
                tiles.remove(i)
                tiles.remove(i)
                return win(tiles)
            # 三元与风牌不组成顺子
            if(i > 30):
                continue
            if(i+1 in tiles and i+2 in tiles):
                tiles.remove(i)
                tiles.remove(i+1)
                tiles.remove(i+2)
                return win(tiles)
    return False


class Wall:
    Tiles = []

    def __init__(self):
        self.Tiles = alltileid

    def shuffle(self):
        for i in range(len(self.Tiles)):
            j = int(random.random() * (i + 1))
            self.Tiles[i], self.Tiles[j] = self.Tiles[j], self.Tiles[i]

    def draw(self, num=1):
        if(num == 1):
            return self.Tiles.pop()
        else:
            temp = self.Tiles[0:num]
            for i in range(num):
                self.Tiles.pop(i)
            return temp

    def left(self):
        return len(self.Tiles)


class Player:
    context = 0
    name = ""
    id = 0
    point = 0
    handTile = []
    showTile = []
    riverTile = []

    def __init__(self, context, name, id, point):
        self.context = context
        self.name = name
        self.id = id
        self.point = point
        self.handTile = []
        self.showTile = []
        self.riverTile = []

    def confirm(self, messages):
        confirmmessage(self.context, messages)
        while(self.context.user_data["confirm"] == -1):
            time.sleep(0.5)
        response = self.context.user_data["confirm"]
        self.context.user_data["confirm"] = 0
        if(response == "True"):
            return True
        else:
            return False

    def organize(self):
        self.handTile.sort()

    def get(self, id):
        self.handTile.append(id)
        self.organize()

    def discard(self):
        sendoption(self.context, "请弃牌：", self.handTile)
        while(self.context.user_data["option"] == -1):
            time.sleep(0.5)
        # print(str(self.context.user_data["option"]))
        id = int(self.context.user_data["option"])
        self.context.user_data["option"] = 0
        self.riverTile.append(id)
        self.handTile.remove(id)
        return id

    def show(self, idlist):
        self.showTile.extend(idlist)
        for i in idlist:
            self.handTile.remove(i)

    def chow(self, id):
        if(id > 30):
            return False
        check = False
        toshow = []
        if(id == self.handTile[0]-1 and self.handTile[0] == self.handTile[1]-1):
            check = True
            toshow = [id, self.handTile[0], self.handTile[1]]
        if(id == self.handTile[-1]+1 and self.handTile[-1] == self.handTile[-2]+1):
            check = True
            toshow = [self.handTile[-2], self.handTile[-1], id]
        for i in range(len(self.handTile)-1):
            if(id == self.handTile[i]+1 and id == self.handTile[i+1]-1):
                check = True
                toshow = [self.handTile[i], id, self.handTile[i+1]]

        if(check == True and self.confirm("吃"+tomahjong(id))):
            self.get(id)
            self.show(toshow)
            return True

    def pong(self, id):
        check = False
        toshow = []
        if(id == self.handTile[0] and id == self.handTile[1]):
            check = True
            toshow = [id, id, id]
        if(id == self.handTile[-1] and id == self.handTile[-2]):
            check = True
            toshow = [id, id, id]
        for i in range(len(self.handTile)-1):
            if(id == self.handTile[i] and id == self.handTile[i+1]):
                check = True
                toshow = [id, id, id]
        if(check == True and self.confirm("碰"+tomahjong(id))):
            self.get(id)
            self.show(toshow)
            return True

    def readyhand(self):
        winningtile = []
        for i in self.handTile:
            winningtile.extend([i-1, i, i+1])
        winningtile = list(set(winningtile))
        wtcopy = list(winningtile)
        for i in winningtile:
            temp = list(self.handTile)
            temp.append(i)
            temp.sort()
            if(win(temp) == False):
                wtcopy.remove(i)
        return wtcopy


class Ai(Player):
    def confirm(self, messages):
        if(random.random() > 0.5):
            return True
        else:
            return False

    def discard(self):
        rtile = int(len(self.handTile)*random.random())
        id = self.handTile[rtile]
        self.riverTile.append(id)
        self.handTile.remove(id)
        return id


class Board:
    id = 0
    wall = Wall()
    players = []
    ongoingTile = 0
    state = "wait"
    ailist =[]

    def __init__(self, id=0, players=[], wall=Wall(),ailist=[Ai(0, "娜瑞提尔", 0, 0), Ai(0, "恩雅", 1, 1), Ai(0, "弥尔米娜", 2, 2),Ai(0, "阿莫恩", 3, 3)]):
        self.id = id
        self.wall = wall
        self.players = list(players)
        self.ailist = list(ailist)

    def add(self, player):
        if(self.state == "playing"):
            return False
        if(player.confirm("准备开始?")):
            print("请求加入board："+str(self.id))
            print(self.players)
            if(self.state == "playing"):
                sendmessage(player.context, "人数已满")
                return False
            player.context.user_data["state"] = "playing"
            self.players.append(player)
            self.broadcast("玩家加入："+str(player.name))
            self.broadcast("人数："+str(len(self.players))+"/4")
            sendmessage(player.context, "已加入Board:"+str(self.id))
            if(len(self.players) == 4):
                self.start()
            return True
        else:
            return False

    def addai(self):
        # 返回是否添加成功
        if(len(self.players) == 4):
            return False
        print(str(self.id)+"剩余ai：")
        print(self.ailist)
        ai = self.ailist.pop()
        self.players.append(ai)
        self.broadcast("AI加入："+str(ai.name))
        self.broadcast("人数："+str(len(self.players))+"/4")
        if(len(self.players) == 4):
            self.start()
        return True

    def broadcast(self, messages):
        for i in self.players:
            if(i.context != 0):
                sendmessage(i.context, str(messages))

    @runasync
    def start(self):
        if(self.state != "wait"):
            return
        self.state = "playing"
        self.broadcast("牌局开始...")
        for i in range(4):
            j = int(random.random() * (i + 1))
            self.players[i], self.players[j] = self.players[j], self.players[i]

        #self.broadcast("顺序："+self.players[0].name+" "+self.players[1].name+" "+self.players[2].name+" "+self.players[3].name)
        self.broadcast("顺序："+str(self.players[0].name)+" "+str(
            self.players[1].name)+" "+str(self.players[2].name)+" "+str(self.players[3].name))
        self.broadcast("洗牌...")
        self.wall.shuffle()
        self.broadcast("发牌...")
        self.deal()

        for i in self.players:
            i.organize()
            self.getboard(i)

        # 主循环
        index = 0
        currentplayer = self.players[index]
        ongoingTile = self.wall.draw()
        # +tomahjong(ongoingTile))
        self.broadcast(str(currentplayer.name)+" 摸牌")
        currentplayer.get(ongoingTile)
        ongoingTile = currentplayer.discard()
        self.broadcast(str(currentplayer.name)+" 弃:"+tomahjong(ongoingTile))
        index = self.next(index)
        while(True):
            for i in self.players:
                self.getboard(i)

            currentplayer = self.players[index]
            # 听牌点炮
            winner = []
            for pl in self.players:
                for i in pl.readyhand():
                    if(ongoingTile == i):
                        if(pl.confirm("胡！")):
                            winner.append(pl)

            if(winner != []):
                for i in winner:
                    self.end(tomahjong(ongoingTile)+str(i.name)+"胡了！")
                    self.broadcast(tomahjong(i.handTile))
                    return

            thenext = index
            flag = ""
            # 碰的处理
            for i in range(3):
                if(self.players[thenext].pong(ongoingTile)):
                    self.players[self.prev(index)].riverTile.remove(
                        ongoingTile)
                    self.broadcast(
                        str(self.players[thenext].name)+"碰"+tomahjong(ongoingTile))
                    ongoingTile = self.players[thenext].discard()
                    self.broadcast(
                        str(self.players[thenext].name)+"弃"+tomahjong(ongoingTile))
                    index = self.next(thenext)
                    flag = "pong"
                    break
                thenext = self.next(thenext)
            if(flag == "pong"):
                continue

            # 吃的处理
            if(currentplayer.chow(ongoingTile)):
                self.players[self.prev(index)].riverTile.remove(ongoingTile)
                self.broadcast(str(currentplayer.name) +
                               "吃"+tomahjong(ongoingTile))
                ongoingTile = currentplayer.discard()
                self.broadcast(str(currentplayer.name) +
                               "弃"+tomahjong(ongoingTile))
                index = self.next(index)
                continue

            # 抽牌
            ongoingTile = self.wall.draw()
            # +tomahjong(ongoingTile))
            self.broadcast(str(currentplayer.name) + " 摸牌")

            # 自摸处理
            for i in currentplayer.readyhand():
                if(ongoingTile == i):
                    if(currentplayer.confirm("胡！")):
                        self.broadcast(tomahjong(ongoingTile))
                        self.end(self.players[thenext].name+"自摸")
                        self.broadcast(
                            tomahjong(self.players[thenext].handTile))
                        return

            # 无事发生
            currentplayer.get(ongoingTile)
            ongoingTile = currentplayer.discard()
            self.broadcast(str(currentplayer.name) +
                           " 弃:"+tomahjong(ongoingTile))

            index = self.next(index)
            if(self.wall.left() == 0):
                winner = []
                for i in self.players:
                    if(i.readyhand() != []):
                        winner.append(str(i.name))
                if(winner == []):
                    self.end("流局：无人胜出")
                else:
                    self.end("流局："+" ".join(winner)+"听牌胜出")
                return

    def end(self, str):
        self.broadcast("游戏结束："+str)
        self.state = "wait"
        for i in self.players:
            if(i.context != 0):
                i.context.user_data["state"] = "wait"
        return

    def next(self, index):
        if(isinstance(index, int)):
            if(index == 3):
                return 0
            else:
                return index+1
        else:
            return list(map(self.next, index))

    def prev(self, index):
        if(index == 0):
            return 3
        else:
            return index-1

    def deal(self):
        for i in self.players:
            i.handTile.extend(self.wall.draw(num=13))

    def getboard(self, player):
        # 除去ai
        if(player.context == 0):
            return
        info = ""
        if(player.name == "娜瑞提尔"):
            for i in self.players:
                info = info+str(i.name)+"\n    " + \
                    tomahjong(i.handTile)+" | "+tomahjong(i.showTile)
                info = info+" 牌河|"+tomahjong(i.riverTile)+"\n"
            sendmessage(player.context, info)
            return
        else:
            infomain = ""
            for i in self.players:
                if(i == player):
                    infomain = str(i.name)+"\n    "+tomahjong(i.handTile)+" | " + \
                        tomahjong(i.showTile)+" 牌河|" + \
                        tomahjong(i.riverTile)+"\n"
                    # printjson({"name": i.name, "handTile": i.handTile,
                    #            "riverTile": i.riverTile})
                else:
                    info = info+str(i.name)+"\n    "+tomahjong(i.showTile) + \
                        " 牌河|"+tomahjong(i.riverTile)+"\n"
                    #printjson({"name": i.name, "riverTile": i.riverTile})
            sendmessage(player.context, infomain+info)


boards = []

# =========================================================bot部分
updater = Updater(token='',
                  use_context=True, request_kwargs={'proxy_url': 'http://127.0.0.1:7890/'})
dispatcher = updater.dispatcher


def start(update, context):
    context.user_data["id"] = update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome to Mahjong!\n你的chatid是："+str(update.effective_chat.id))


def play(update, context):
    context.user_data["confirm"] = 0
    context.user_data["option"] = 0
    context.user_data["id"] = update.effective_chat.id
    if(not context.user_data.get("name")):
        sendmessage(context, "先设置一个名字吧\n/setname [yourname]")
        return
    
    if(context.user_data.get("state", "wait") == "playing"):
        sendmessage(context, "已经在游戏中了")
        return
    player = Player(context, context.user_data.get("name"), update.effective_chat.id, 0)

    for i in range(len(boards)):
        if(boards[i].state == "playing"):
            #print("游戏进行中:"+str(i))
            continue
        else:
            context.user_data["board"] = i
            #print("列表内board.add调用完成:"+str(i))
            return True
    id = len(boards)
    newboard = Board(id=int(id))
    #print("创建newboard:"+str(newboard.id))
    boards.append(newboard)
    newboard.add(player)
    context.user_data["board"] = newboard.id
    #print("newboard.add已调用:"+str(newboard.id))
    return


def addai(update, context):
    if(context.user_data.get("state", "wait") == "wait"):
        sendmessage(context, "请先开始游戏")
        return
    boardid = int(context.user_data.get("board", -1))
    if(boardid != -1):
        #print("尝试添加ai:"+str(boardid))
        board = boards[boardid]
        board.addai()
        #print("board.addai已调用:"+str(boardid))
    else:
        sendmessage(context, "ai加入失败，请重试")


def sendoption(context, messages, options):
    context.user_data["option"] = -1
    id = context.user_data.get("id")
    keyboard = [[], []]
    options = options+[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    op1 = options[0:7]
    op2 = options[7:15]
    for i in op1:
        if(i == 0):
            break
        keyboard[0].append(InlineKeyboardButton(
            tomahjong(i), callback_data=str(i)))
    for i in op2:
        if(i == 0):
            break
        keyboard[1].append(InlineKeyboardButton(
            tomahjong(i), callback_data=str(i)))
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(id, messages, reply_markup=reply_markup)


def sendmessage(context, messages):
    id = context.user_data.get("id")
    context.bot.send_message(id, messages)


def confirmmessage(context, messages):
    context.user_data["confirm"] = -1
    id = context.user_data.get("id")
    keyboard = [[InlineKeyboardButton("是", callback_data='True'),
                 InlineKeyboardButton("否", callback_data='False')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(id, text=messages, reply_markup=reply_markup)


def setname(update, context):
    context.user_data["id"] = update.effective_chat.id
    value = update.message.text.partition(' ')[2]
    if(value==""):value=update.effective_user.first_name
    context.user_data["name"] = value
    update.message.reply_text("昵称修改为："+value)
    if(value == "娜瑞提尔"):
        sendmessage(context, "为什么不看看他们的手牌呢？")


def getname(update, context):
    value = context.user_data.get("name", 'Not found')
    update.message.reply_text(value)


def button(update, context):
    query = update.callback_query
    if context.user_data["confirm"] == -1:
        context.user_data["confirm"] = query.data
        if(query.data == "True"):
            query.edit_message_text(text="已确认")
        else:
            query.edit_message_text(text="已取消")
        time.sleep(2)
        query.delete_message()
        return
    if context.user_data["option"] == -1:
        context.user_data["option"] = query.data
        boardid = int(context.user_data.get("board", -1))
        board = boards[boardid]
        query.edit_message_text(
            text="你选择: {}".format(tomahjong(int(query.data)))+"   剩余张数："+str(board.wall.left()))
        time.sleep(2)
        query.delete_message()
        return


def restartboard(update, context):
    boardid = int(context.user_data.get("board", -1))
    board = boards[boardid]
    board.end("restart")
    boards.remove(board)


dispatcher.add_handler(CommandHandler('setname', setname, run_async=True))
dispatcher.add_handler(CommandHandler('getname', getname, run_async=True))
dispatcher.add_handler(CommandHandler('addai', addai, run_async=True))
dispatcher.add_handler(CommandHandler('play', play, run_async=True))
dispatcher.add_handler(CommandHandler('start', start, run_async=True))
dispatcher.add_handler(CommandHandler(
    'restartboard', restartboard, run_async=True))
dispatcher.add_handler(CallbackQueryHandler(button, run_async=True))
updater.start_polling()
