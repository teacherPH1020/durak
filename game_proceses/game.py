import random
from config import *

def deal(players,deck,table):
    """раздает карты в начале игры игрокам из колоды,выбирает козырь"""
    global trump, SUITS,NUMBERS
    if len(deck)< len(SUITS) * len(NUMBERS): return "missing cards in deck"
    elif len(table)>0: return  "table is not empty"
    elif len(players)<2:return "need more than one player"
    for _ in range(6):
        for p in players:
            p["hand"].append(deck.pop(0))
    trump = deck.pop(0)
    deck.append(trump)
    return "dealt 6 cards to each player, trump from" + str(trump)

def compare(card_bottom,card_top)->"True if top beats bottom":
    """сравниваем две картыбесли верхняя бъет нижнюю"""
    global trump,SUIT,NUM
    if trump is None:
        print("trump is not closen,cant compare")
        return None
    beats = False
    if (card_bottom[SUIT] != card_top[SUIT]) and (card_top[SUIT] is not trump[SUIT]): beats = False
    elif (card_top[SUIT] is trump[SUIT]) and (card_bottom[SUIT] is not trump[SUIT]):beats = True
    elif (card_bottom[SUIT] == card_top[SUIT]) and (NUMBERS.index(card_top[NUM])> NUMBERS.index(card_bottom[NUM])):beats = True
    return beats

def table_view(table,d = None):
    """выводит вид стола"""
    print("\tВ колоде " + str(d))
    print(f"\tКозырная{trump}")
    print("\tСтол")
    print("\t\tатаки", table[0::2])
    print("\t\tотбой", table[1::2])

def hand_view(hand):
    """выводит карты на руках"""
    for i,c in enumerate(hand):
        print(f"{i+1} = {c}",end= ":")
    print("О=взять/ок","x=end game")

def goes_first(players):
    """решаем кто идет первым"""
    for n,p in enumerate(players):
        if p["last"]:
            p["last"] = False
            return n
    return random.randint(0,len(players)-1)

def card_match(table,hand,opt = 0):
    """ищет по совпадению"""
    t = [c[opt] for c in table]
    for i,h in enumerate(hand):
        if h[opt] in t: return i
    return None

def attack(who,players,table):
    """ataka"""
    global NUM
    hand = players[who]["hand"]
    if len(hand) ==0: return "empty"
    #computer
    if who ==0:
        if len(table) ==0:
            n = random.randint(0,len(hand)-1)
            table.append(hand[n])
            players[who]["hand"].pop(n)
        else:
            n = card_match(table,hand,NUM)
            if n is not None:
                table.append(hand[n])
                players[who]["hand"].pop(n)
            else:
                return "done"
    #human
    else:
        n =0
        while True:
            pick = input(PROMPT)
            try:
                if int(pick) == 0: return "done"
            except:
                pass
            if pick.isnumeric():
                n = int(pick)-1
            elif pick.lower() == "x" or pick.lower() == "х" :
                print("Exiting game")
                exit(-1)
            else:
                print("Enter correct choice")
                n = -1
            if n<0 or n> len(hand)-1:continue
            if len(table) == 0: break
            c = hand[n]
            if card_match(table,[c],NUM) is not None: break

        table.append(hand[n])
        players[who]["hand"].pop(n)
    return "attack"

def defend(who,players,table):
    """отбиваемся"""
    if len(table) == 0: return "no attacks"
    hand = players[who]["hand"]
    if len(hand) ==0: return "out of cards"
    #computer
    if who ==0:
        pick = None
        for i,c in enumerate(hand):
            if compare(table[-1],c):
                pick = players[who]["hand"].pop(i)
                break
        if pick is not None:
            table.append(pick)
        else:
            return "taking"
    #human
    else:
        while True:
            pick = input(PROMPT)

            if pick.isnumeric():
                n = int(pick) - 1
            elif pick.lower() == "x" or pick.lower() == "х" :
                print("Exiting game")
                exit(-1)
            else:
                print("Enter correct choice")
                n = -1
            if n<0 or n>len(hand)-1:continue
            if int(pick) == 0: return "taking"
            if compare(table[-1],hand[n]):break
        table.append(hand[n])
        players[who]["hand"].pop(n)
    return "defence"

def count_empty(players):
    """считает игроков без карт"""
    c = 0
    for p in players:
        if len(p["hand"]) == 0: c+=1
    return c

def defending(attacker,n):
    """кто отбивается"""
    return (attacker+1)%n

def count_battles():
    b = 0
    while True:
        b+=1
        yield b

def battle(attacker,players,table,deck,played,count):
    """битва"""
    print("Битва №",next(count))
    n_players = len(players)
    table_view(table,len(deck))
    while True:
        hand_view(players[1]["hand"])
        ###hand_view(players[0]["hand"])
        a_out = attack(attacker,players,table)
        d_out = ""
        print(a_out)###
        table_view(table,len(deck))
        hand_view(players[1]["hand"])
        ###hand_view(players[0]["hand"])
        if a_out == "attack":
            defendant = defending(attacker,n_players)
            d_out = defend(defendant,players,table)
            print(d_out)###
            if d_out == "out of cards":
                players[attacker]["hand"].append(table.pop(0))
            elif d_out == "taking":
                nxt = attacker
                players[defendant]["hand"].extend(table)
                table.clear()
                break
        if a_out == "done" or a_out == "empty" or d_out == "out of cards":
            played.extend(table)
            table.clear()
            nxt = (attacker+1)% n_players
            break
        table_view(table,len(deck))
    return {"attacker":attacker,"next": nxt}

def take(result,players,table,deck):
    """пополнение карт по очереди"""
    turn = result["attacker"]
    while True:
        if len(deck) ==0:
            break
        if len(players[turn]["hand"])<6:
            card = deck.pop(0)
            players[turn]["hand"].append(card)
            continue
        turn+=1
        if turn >len(players)-1: turn = 0
        if turn == result["attacker"]:break
    return len(deck)==0

def meet_players(players):
    """создаем игроков"""
    if len(players)>0: players.clear()
    players.append(dict(name = "Компьютер", fool = 0,last = False,hand = []))
    name = ""
    while name =="": name = input("Введите ваше имя: ")
    ### name = "Alex"###
    players.append(dict(name = name, fool = 0, last = False, hand = []))
    print("ИГРОКИ:")
    for n,p in enumerate(players):
        print(f"\t{n+1}.{p['name']}")




