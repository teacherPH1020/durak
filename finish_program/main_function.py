def main(*args):
    "партии игры"
    #print(args)
    print("ИГРА ДУРАК")
    #дураков пока нет
    fool = None
    #счетчик генератор
    count = count_battles()
    #колода
    deck = []
    #битые карты
    played = []
    # стол
    table = []
    #игроки
    players = []
    meet_players(players)
    #партии
    more = "yes"
    while more == "yes":
        print(create_deck(deck))#достаем колону
        print(shuffle(deck)) # мешаем колоду
        print(deal(players,deck,table))#раздаем колоду
        attacker = goes_first(players)#кто ходит первым
        done = False
        while not done:
            result = battle(attacker,players,table,deck,played,count)
            attacker = result["next"]#кто следующий
            if take(result,players,table,deck) and count_empty(players) >= len(players)-1:
                done = True
                fool = None
                for i,p in enumerate(players):
                    if len(p["hand"]) !=0:fool = i
            #done = True### отладка
        #fool = 1###
        if fool is None:
            print("Ничья - дураков нет")
        else:
            players[fool]["last"] = True
            players[fool]["fool"] += 1
            print("Дурак этой партии это",players[fool]["name"])
        played.clear()  # убираем отыгранные карты
        table.clear()  # чистый стол
        print("ИГРА ЗАВЕРШЕНА")
        more = input("Введите yes для ещё одной партии:")

#glory_table(players)#доска результатов


