RANK = {
    "nothing": 1,
    "jutt": 2,
    "color": 3,
    "run": 4,
    "double_run": 5,
    "trail": 6
}

VAL = {
    "1": 14, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "11": 11, "12": 12, "13": 13
}

def parse(cards):
    v, s = [], []
    for c in cards:
        v.append(VAL[c[:-1]])
        s.append(c[-1])
    v.sort()
    return v, s

def run(v):
    return (
        v[0]+1 == v[1] == v[2]-1 or
        v == [2,3,14] or
        v == [12,13,14]
    )

def run_strength(v):
    if v == [2,3,14]: return [3,2,1]
    if v == [12,13,14]: return [14,13,12]
    return v[::-1]

def eval_hand(cards):
    v, s = parse(cards)
    if v[0]==v[1]==v[2]:
        return (RANK["trail"], [v[0]], "TRAIL")
    if run(v) and len(set(s))==1:
        return (RANK["double_run"], run_strength(v), "PURE RUN")
    if run(v):
        return (RANK["run"], run_strength(v), "RUN")
    if len(set(s))==1:
        return (RANK["color"], v[::-1], "COLOR")
    if len(set(v))==2:
        pair = max(v, key=v.count)
        kick = min(v, key=v.count)
        return (RANK["jutt"], [pair, kick], "JUTT")
    return (RANK["nothing"], v[::-1], "HIGH CARD")

def find_winner(players):
    scores = {n: eval_hand(c) for n,c in players.items()}
    winner = max(scores.items(), key=lambda x:(x[1][0], x[1][1]))
    return winner, scores
