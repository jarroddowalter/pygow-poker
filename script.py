import random
from rich import print
from rich.console import Console

console = Console()

DECK = [
'2♥', '2♦', '2♠', '2♣',
'3♥', '3♦', '3♠', '3♣',
'4♥', '4♦', '4♠', '4♣',
'5♥', '5♦', '5♠', '5♣',
'6♥', '6♦', '6♠', '6♣',
'7♥', '7♦', '7♠', '7♣',
'8♥', '8♦', '8♠', '8♣',
'9♥', '9♦', '9♠', '9♣',
'10♥', '10♦', '10♠', '10♣',
'J♥', 'J♦', 'J♠', 'J♣',
'Q♥', 'Q♦', 'Q♠', 'Q♣',
'K♥', 'K♦', 'K♠', 'K♣',
'A♥', 'A♦', 'A♠', 'A♣',
'JKR',
]


def deal_game():
	game_deck = DECK.copy()
	random.shuffle(game_deck)

	player_hand = game_deck[:7]
	del game_deck[:7]
	dealer_hand = game_deck[:7]
	del game_deck[:7]

	print("Dealer: ", end='')
	pretty_print_hand(dealer_hand)
	print()
	print("Player: ", end='')
	pretty_print_hand(player_hand)

def pretty_print_hand(hand):
	for i, card in enumerate(hand):
		if card[-1] == "♠" or card[-1] == "♣":
			console.print(" " + card + " ", style="black on white b", end='')
		elif card[-1] == "♥" or card[-1] == "♦":
			console.print(" " + card + " ", style="red on white b", end='')
		elif card == "JKR":
			console.print(" " + card + " ", style="black on white b", end='')\
		
		if len(hand) != i+1:
			console.print(" ", end='')
		else:
			console.print()

deal_game()
