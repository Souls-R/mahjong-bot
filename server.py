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
    if(isinstance(id, int)):
        return alltile[int(id/10)][id % 10]
    else:
        return list(map(tomahjong, id))


def printjson(obj):
    print(obj)
    #print(json.dumps(obj))


def win(tiles):
    if(len(tiles)==14):
        for i in range(len(tiles)-1):
            if(tiles[i] == tiles[i+1]):
                pair=tiles[i]
                temp = list(tiles)
                del temp[i:i+2]
                if(win(temp)):
                    #log
                    #print("HU pair:"+str(pair))
                    return True
        return False
    
    if(len(tiles)<=12):
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
            temp = self.Tiles[0:num-1]
            for i in range(num):
                self.Tiles.pop(i)
            # log
            print(" ".join(tomahjong(temp)))
            return temp


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

    def organize(self):
        self.handTile.sort()

    def draw(self, id):
        self.handTile.append(id)

    def discard(self, id=0):
        if(id == 0):
            id = self.handTile[0]
        # log
        print(self.name+" dicord:"+str(id))
        self.riverTile.append(id)
        self.handTile.remove(id)

    def show(self, idlist):
        showTile.extend(idlist)
        for i in idlist:
            handTile.remove(i)

    def readyhand(self):
        winningtile=[]
        for i in self.handTile:winningtile.extend([i-1,i,i+1])
        winningtile=list(set(winningtile))
        wt=list(winningtile)
        for i in winningtile:
            temp=list(self.handTile)
            temp.append(i)
            temp.sort()
            if(win(temp)==False):wt.remove(i)
        return wt
    
    # def chow():


class Board:
    wall = Wall()
    players = []
    ongoingTile = 0

    def __init__(self, players=[Player("恩雅", 1, 1), Player("弥尔米娜", 2, 2), Player("阿莫恩", 3, 3), Player("娜瑞提尔", 4, 4)], wall=Wall()):
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
        while(True):
            self.getboard(1)
            self.players[1].discard()
            self.players[1].discard()
            self.players[2].discard()
            self.players[3].discard()
            self.getboard(4)
            break

    def deal(self):
        for i in self.players:
            i.handTile.extend(self.wall.draw(num=13))

    def getboard(self, playerid=0):
        for i in self.players:
            if(i.id == playerid):
                printjson({"name": i.name, "handTile": i.handTile,
                           "riverTile": i.riverTile})
            else:
                printjson({"name": i.name, "riverTile": i.riverTile})


# board = Board()
# board.start()

player = Player("test", 1, 1)
player.handTile=[1,2,3,4,5,6,9,11,12,13,14,32,32]
print(player.readyhand())
player.handTile=[1,2,3,4,5,6,7,11,12,13,41,41,41]
print(player.readyhand())