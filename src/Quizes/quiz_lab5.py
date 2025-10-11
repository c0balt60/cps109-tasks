def faro_shuffle(cards: list[int|str|None], out: bool):
    l = len(cards) // 2

    left, right = cards[:l], cards[l:]
    ret = []

    for x,y in zip(left, right):
        ret.append(x if out else y)
        ret.append(y if out else x)
    
    if len(cards) % 2 != 0:
        ret.append(right[-1])

    return ret

out1 = faro_shuffle([1,2,3,4,5], True)
out2 = faro_shuffle(["bob", "jack", "daniel"], False)
print(out1)
