import blackjack as bj
import random

def game():
  player = Player(1000)
  dealer = Player(0)
  deck = Deck()
  roundNumber = 1
  while True:
    print(f"Round {roundNumber}")
    if (roundNumber - 1) % 10 == 0:
      random.shuffle(deck.cards)
    bj.clear_hand(player)
    bj.clear_hand(dealer)
    bj.bet(player)
    bj.start_round(player, dealer, deck)
    if bj.check_naturals(player, dealer):
      pass
    else:
      bj.player_move(player, deck, 0)
      bj.dealer_move(dealer, deck)
      bj.check_winner(player, dealer)
    if player.balance < 5:
      print("You ran out of money. Better luck next time!") 
      break
    if bj.replay():
      roundNumber += 1 
    else:
      break
    bj.clear()

class Player:
  def __init__(self, balance):
    self.hand = [[],[],[],[]]
    self.value = [0,0,0,0]
    self.balance = 1000
    self.bet = 0
    self.insurance = 0
  
  def show_hand(self, i):
    for c in self.hand[i]:
        print(c)
    return ""

class Card:
  def __init__(self, val, suit):
    self.value = val
    self.suit = suit

  def __str__ (self):
    return f"     [{self.value} {self.suit}]"

class Deck:
  def __init__(self):
    self.cards = []
    self.build()
    
  def build(self):
    for s in ["Spades","Clubs","Diamonds","Hearts"]:
      for i in range(0,6):
        for v in range(2,11):
          self.cards.append(Card(v,s))
        for v in ["J","Q","K","A"]:
          self.cards.append(Card(v,s))

  def __str__ (self):
    for c in self.cards:
      print(c) 
    return ""

if __name__ == "__main__":
  game()