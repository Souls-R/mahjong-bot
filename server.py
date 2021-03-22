import random
import json

# 🀀🀁🀂🀃🀄🀅🀆🀇🀈🀉🀊🀋🀌🀍🀎🀏🀐🀑🀒🀓🀔🀕🀖🀗🀘🀙🀚🀛🀜🀝🀞🀟🀠🀡🀢🀣🀤🀥🀦🀧🀨🀩🀪 🀫
alltileid = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29,
             31, 32, 33, 34, 41, 42, 43]
"""
01-09 : 万子
11-19 : 条子
21-29 : 筒子
31-34 : 风牌
41-43 : 三元
"""
character = [0, "🀇", "🀈", "🀉", "🀊", "🀋", "🀌", "🀍", "🀎", "🀏"]
bamboo = [0, "🀐", "🀑", "🀒", "🀓", "🀔", "🀕", "🀖", "🀗", "🀘"]
dot = [0, "🀙", "🀚", "🀛", "🀜", "🀝", "🀞", "🀟", "🀠", "🀡"]
wind = [0, "🀀", "🀁", "🀂", "🀃"]
dragon = [0, "🀄", "🀅", "🀆"]
alltile = [character, bamboo, dot, wind, dragon]


def tomahjong(id):
    #将麻将id或id列表转换为emoji
    if(isinstance(id, int)):
        return alltile[int(id/10)][id % 10]
    else:
        return list(map(tomahjong, id))


def printjson(obj):
    #将对象json序列化输出
    print(obj)
    # print(json.dumps(obj))

def win(tiles):
#接受14张已排序的牌 返回是否胡牌
    if(len(tiles) == 14):
        for i in range(len(tiles)-1):
            if(tiles[i] == tiles[i+1]):
                pair = tiles[i]
                temp = list(tiles)
                del temp[i:i+2]
                if(win(temp)):
                    # log
                    #print("HU pair:"+str(pair))
                    return True
        return False

    if(len(tiles) <= 12):
        if(len(tiles) == 0):
            return True
        for i in range(len(tiles)-2):
            if(tiles[i] == tiles[i+1] and tiles[i+1] == tiles[i+2]):
                del tiles[i:i+3]
                return win(tiles)
            # 三元与风牌不组成顺子
            if(tiles[i] > 30):
                continue

            if(tiles[i] == tiles[i+1]-1 and tiles[i+1] == tiles[i+2]-1):
                del tiles[i:i+3]
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
            # log
            print(" ".join(tomahjong(temp)))
            return temp

    def left(self):
        return len(self.Tiles)


class Player:
    name = ""
    id = 0
    point = 0
    handTile = []
    showTile = []
    riverTile = []

    def __init__(self, name, id, point):
        self.name = name
        self.id = id
        self.point = point
        self.handTile = []
        self.showTile = []
        self.riverTile = []

    def confirm(self,messages):
        printjson({"message":messages})
        #接入bot
        response=input()
        if(response=="y"):return True
        elif(response=="n"):return False
        else:return int(response)


    def organize(self):
        self.handTile.sort()

    def get(self, id):
        self.handTile.append(id)
        self.organize()

    def discard(self):
        id=self.confirm("选择弃牌（id）：")
        # log
        print(self.name+" 弃:"+tomahjong(id))
        self.riverTile.append(id)
        self.handTile.remove(id)
        return id

    def show(self, idlist):
        print("show:")
        print(" ".join(tomahjong(idlist)))
        print(" ".join(tomahjong(self.handTile)))
        self.showTile.extend(idlist)
        for i in idlist:
            self.handTile.remove(i)


    def chow(self, id):
        if(id>30):return False
        check=False
        toshow=[]
        if(id==self.handTile[0]-1 and self.handTile[0]==self.handTile[1]-1):
            check=True
            toshow=[id,self.handTile[0],self.handTile[1]]
        if(id==self.handTile[-1]+1 and self.handTile[-1]==self.handTile[-2]+1):
            check=True
            toshow=[self.handTile[-2],self.handTile[-1],id]
        for i in range(len(self.handTile)-1):
            if(id==self.handTile[i]+1 and id==self.handTile[i+1]-1):
                check=True
                toshow=[self.handTile[i],id,self.handTile[i+1]]

        if(check==True and self.confirm("chow")):
            #log
            print(self.name+"吃"+tomahjong(id))
            self.get(id)
            self.show(toshow)
            return True

    def pong(self, id):
        check=False
        toshow=[]
        if(id==self.handTile[0] and id==self.handTile[1]):
            check=True
            toshow=[id,id,id]
        if(id==self.handTile[-1] and id==self.handTile[-2]):
            check=True
            toshow=[id,id,id]
        for i in range(len(self.handTile)-1):
            if(id==self.handTile[i] and id==self.handTile[i+1]):
                check=True
                toshow=[id,id,id]
        if(check==True and self.confirm("pong")):
            #log
            print(self.name+"碰"+tomahjong(id))
            self.get(id)
            self.show(toshow)
            return True
    
    def readyhand(self):
        winningtile = []
        for i in self.handTile:
            winningtile.extend([i-1, i, i+1])
        winningtile = list(set(winningtile))
        wt = list(winningtile)
        for i in winningtile:
            temp = list(self.handTile)
            temp.append(i)
            temp.sort()
            if(win(temp) == False):
                wt.remove(i)
        return wt

class Ai(Player):
    def confirm(self,messages):
        if(random.random()>0.5):return True
        else:return False

    def discard(self):
        rtile=int(len(self.handTile)*random.random())
        id = self.handTile[rtile]
        # log
        print(self.name+" 弃:"+tomahjong(id))
        self.riverTile.append(id)
        self.handTile.remove(id)
        return id


class Board:
    wall = Wall()
    players = []
    ongoingTile = 0

    def __init__(self, players=[Ai("恩雅", 1, 1), Ai("弥尔米娜", 2, 2), Ai("阿莫恩", 3, 3), Player("娜瑞提尔", 4, 4)], wall=Wall()):
        self.wall = wall
        self.players = players



    def start(self):
        printjson({"messages": "牌局开始..."})

        for i in range(len(self.players)):
            j = int(random.random() * (i + 1))
            self.players[i], self.players[j] = self.players[j], self.players[i]
        ordermessege = {"messages": "顺序："+self.players[0].name+" " +
                        self.players[1].name+" "+self.players[2].name+" "+self.players[3].name}
        printjson(ordermessege)
        printjson({"messages": "洗牌..."})
        self.wall.shuffle()
        printjson({"messages": "发牌..."})
        self.deal()

        for i in self.players:
            i.organize()
            printjson(i.__dict__)

        # 主循环
        index = 0
        ongoingTile = 0
        while(True):
            #self.getboard(self.players[index].id)
            if(self.players[index].id==4):self.getboard(4)
            currentplayer=self.players[index]

            #听牌点炮
            winner=[]
            for i in currentplayer.readyhand():
                if(ongoingTile==i):
                    if(currentplayer.confirm("win")):
                        winner.append(currentplayer)
            
            if(winner!=[]):
                print(tomahjong(ongoingTile))
                for i in winner:
                    self.end(i.name+"点炮")
                    printjson(" ".join(tomahjong(self.players[thenext].handTile)))
                    return

            
            thenext=index
            flag=""
            #碰的处理
            for i in range(3):
                if(self.players[thenext].pong(ongoingTile)):
                    ongoingTile=self.players[thenext].discard()
                    index=self.next(thenext)
                    flag="pong"
                    break
                thenext=self.next(thenext)
            if(flag=="pong"):continue
            

            #吃的处理
            if(currentplayer.chow(ongoingTile)):
                ongoingTile=currentplayer.discard()
                index=self.next(index)
                continue
            
            #抽牌
            ongoingTile = self.wall.draw()
            # log
            print(currentplayer.name+" 摸:"+tomahjong(ongoingTile))
            #自摸处理
            for i in currentplayer.readyhand():
                if(ongoingTile==i):
                    if(currentplayer.confirm("win")):
                        print(tomahjong(ongoingTile))
                        self.end(self.players[thenext].name+"自摸")
                        printjson(" ".join(tomahjong(self.players[thenext].handTile)))
                        return
        

            #无事发生
            currentplayer.get(ongoingTile)
            ongoingTile = currentplayer.discard()


            index = self.next(index)
            if(self.wall.left() == 0):
                winner=[]
                for i in self.players:
                    if(i.readyhand()!=[]):winner.append(i.name)
                if(winner==[]):self.end("流局：无人胜出")
                else:self.end("流局："+" ".join(winner)+"听牌胜出")
                return

    def end(self,str):
        print("游戏结束："+str)
        return

    def next(self,index):
        if(isinstance(index, int)):
            if(index==3):return 0
            else: return index+1
        else:
            return list(map(self.next, index))

    def deal(self):
        for i in self.players:
            i.handTile.extend(self.wall.draw(num=13))

    def getboard(self, playerid=0):
        if(playerid==0):
            for i in self.players:
                print(i.name+"手牌"+" ".join(tomahjong(i.handTile))+"     副露区"+" ".join(tomahjong(i.showTile)))
                print("     牌河"+" ".join(tomahjong(i.riverTile)))
                #printjson({"name": i.name, "handTile": i.handTile,"riverTile": i.riverTile})
            return
        for i in self.players:
            if(i.id == playerid):
                print(i.name+"手牌"+" ".join(tomahjong(i.handTile))+"     副露区"+" ".join(tomahjong(i.showTile)))
                print("     牌河"+" ".join(tomahjong(i.riverTile)))
                # printjson({"name": i.name, "handTile": i.handTile,
                #            "riverTile": i.riverTile})
            else:
                print(i.name+"副露区"+" ".join(tomahjong(i.showTile))+"     牌河"+" ".join(tomahjong(i.riverTile)))
                #printjson({"name": i.name, "riverTile": i.riverTile})

board = Board()
board.start()