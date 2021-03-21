
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
print(tomahjong(22))