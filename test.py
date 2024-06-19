import math


def trans_card_to_points(card_num):
    if card_num <= 36:  # 1 -> 10
        card_num /= 4
        card_num = math.ceil(card_num + 1)
    elif 37 <= card_num <= 48:  # 10 -> K
        card_num = 10
    print(card_num)


trans_card_to_points(12)
