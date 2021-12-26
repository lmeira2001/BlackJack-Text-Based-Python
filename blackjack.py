from os import system, name

def clear():
  if name == 'nt':
    _ = system('cls')
  else:
    _ = system('clear')

def replay():
  while True:
    inp = input("Do you want to keep playing (Y,N)? ")
    if inp in ["N","n"]:
      clear()
      return False
    elif inp in["Y","y"]:
      return True
    else:
      print("Please introduce a valid option.")

def bet(player):
  print(f"Current balance: ${player.balance}")
  while True:
    bet = input("How much do you want to bet? ")
    try: 
      player.bet = int(bet)
    except:
      print("Please introduce a number. ")
    else:
      bet = int(bet)   
      if bet <= player.balance:
        if bet > 4:
          break
        else:
          print("Bet minimum is $5.")
      else:
        print("You don't have enough balance. The value is too large.")
  print(f"You are betting ${bet}")

def insurance(player):
  while True:
    insurance = input("How much do you want to insure? ")
    try: 
      player.insurance = int(insurance)
    except:
      print("Please introduce a number. ")
    else:
      insurance = int(insurance)
      if insurance <= player.balance:
        if insurance > -1:
          if insurance <= (player.bet / 2):
            break
          else: 
            print("Your max insurance is half of your bet.")
        else:
          print("You need to make a bet a positive amount.")
      else:
        print("You don't have enough balance. The value is too large.")
  print(f"You are insuring ${insurance}")

def give_cards(player, deck, i, hand):
  for i in range(0,i):
    player.hand[hand].append(deck.cards[0])
    deck.cards.append(deck.cards[0])
    deck.cards.pop(0)
  set_value(player)

def set_value(player):
  for j in range(0,4):
    player.value[j] = 0
    unusedAces = 0
    for i in player.hand[j]:
      if i.value in ["J","Q","K"]:
        player.value[j] += 10;
      elif i.value == "A":
        player.value[j] += 11
        unusedAces += 1
      else:
        player.value[j] += int(i.value);
    if player.value[j] > 21 and unusedAces != 0:
      while player.value[j] > 21 and unusedAces != 0:
        player.value[j] -= 10
        unusedAces -= 1;

def start_round(player, dealer, deck):
  give_cards(player,deck,2,0)
  print("Your Cards:")
  player.show_hand(0)
  give_cards(dealer,deck,2,0)
  print("Dealers Card:")
  print(f"{dealer.hand[0][0]}")

def check_naturals(player,dealer):
  if dealer.hand[0][0].value == "A":
    insurance(player)
  if dealer.value[0] == 21:
    if player.value[0] != 21: 
      lost(player)
    else:
      tie(player)
    ret = True
  elif player.value[0] == 21:
    win(player)
    ret = True
  else:
    player.balance -= player.insurance
    player.insurance = 0
    ret = False
  return ret

  player.insurance = 0

def dealer_move(dealer,deck):
  while True:
    if dealer.value[0] < 17:
      give_cards(dealer,deck,1,0)
    else:
      break
  print("Dealer's Cards:")
  for i in dealer.hand[0]:
    print(i)

def player_move(player, deck, hand):
  while True:
    if player.hand[hand][0].value == player.hand[hand][1].value and hand == 0 and player.balance >= 2 * player.bet and len(player.hand[hand]) == 2:
      move = input("Do you want to Hit (H), Stand (St) or Double (D), or Split (Sp)? ")
    elif player.balance >= 2 * player.bet and len(player.hand[hand]) == 2 and hand == 0:
      move = input("Do you want to Hit (H), Stand (St) or Double (D)? ")
    else:
      move = input("Do you want to Hit (H), Stand (St)? ")
    if move in ["St", "st"]:
      break
    elif move in ["H","h"]:
      hit(player, deck, hand)
      if player.value[hand] > 21:
        break   
    elif move in ["Sp", "sp"]:
      split(player, deck, hand)
      break
    elif move in ["D", "d"]:
      double(player, deck, hand)
      break
    else:
      print("Please enter a valid option.")

def hit(player, deck, hand):
  give_cards(player, deck, 1, hand)
  print("Your Cards:")
  player.show_hand(hand)

def split(player, deck, hand):
      hand2 = 0
      if hand == 0 and player.value[1] == 0:
        hand2 = 1
      elif hand == 0 and player.value[1] != 0:
        hand2 = 2        
      elif hand == 1:
        hand2 = 3
      player.hand[hand2].append(player.hand[hand][1])
      player.hand[hand].pop(1)
      give_cards(player, deck, 1, hand)
      give_cards(player, deck, 1 ,hand2)
      print("First Hand:")
      player.show_hand(hand)
      player_move(player, deck, hand)
      print("Second Hand:")
      player.show_hand(hand2)      
      player_move(player, deck, hand2)

def double(player, deck, hand):
  player.bet += player.bet
  give_cards(player,deck,1,hand)
  print("Your Cards:")
  player.show_hand(hand)

def check_winner(player,dealer):
  for i in range(0,4):
    if player.value[i] == 0:
      pass
    elif player.value[i] > 21:
      lost(player)
    elif dealer.value[0] > 21:
      win(player)
    elif player.value[i] > dealer.value[0]:
      win(player)
    elif dealer.value[0] > player.value[i]:
      lost(player)
    elif dealer.value[0] == player.value[i]:
      tie(player)

def lost(player):
  print("Dealer wins.")
  player.balance -= player.bet - 2 * player.insurance
  print(f"Current balance: ${player.balance}")

def tie(player):
  print("It's a tie.")
  print(f"Current balance: ${player.balance}")

def win(player):
  print("You win.")
  player.balance += player.bet * (1 / 2) - player.insurance
  print(f"Current balance: ${player.balance}")
  
def clear_hand(player):
  j = 0
  for i in player.hand:
    player.hand[j].clear()
    j += 1
  player.bet = 0
  player.insurance = 0
  player.value = [0,0,0,0]