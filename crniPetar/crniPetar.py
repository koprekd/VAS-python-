#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import spade
import time
import player
from deck import deck

def ShuffleDeck(deck):
    random.shuffle(deck)
    return deck

def DealCards(player1, player2, deck):
    deck = ShuffleDeck(deck)
    dealTo = player1
    for card in deck:
        dealTo.addCardToHand(card)
        dealTo = player2 if dealTo == player1 else player1
    
def InitializeGame(player1, player2, deck):
    print("~~~Igra počinje!~~~")
    time.sleep(2)
    print(f"IGRAČI: {player1.name} i {player2.name}")
    time.sleep(2)
    print("***Dijelim karte***")
    DealCards(player1, player2, deck)
   

if __name__ == '__main__':   
    
    player1 = player.Player("dakoprek@localhost", "123456", True, "dakoprek2@localhost")
    player2 = player.Player("dakoprek2@localhost", "123456", False, "dakoprek@localhost")

    InitializeGame(player1, player2, deck)

    input("Pritisnite ENTER za početak. Kad se odvrti igra ponovno pritisnite ENTER za kraj.\n")
    player1.start()
    time.sleep(2)
    player2.start()
    input("")
    player1.stop()
    player2.stop() 
    spade.quit_spade()
