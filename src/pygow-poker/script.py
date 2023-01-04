import random

class Card:
	def __init__(self, value: int, suit: str):
		self.value = value
		self.suit = suit

	def pretty(self): ##returns pretty string of card
		pretty_card = ""

		match self.value:  ## convert num
			case 2:
				pretty_card = " 2"
			case 3:
				pretty_card = " 3"
			case 4:
				pretty_card = " 4"
			case 5:
				pretty_card = " 5"
			case 6:
				pretty_card = " 6"
			case 7:
				pretty_card = " 7"
			case 8:
				pretty_card = " 8"
			case 9:
				pretty_card = " 9"
			case 10:
				pretty_card = "10"
			case 11:
				pretty_card = " J"
			case 12:
				pretty_card = " Q"
			case 13:
				pretty_card = " K"
			case 14:
				pretty_card = " A"
			case 0:
				pretty_card = "JKR"

		match self.suit:  ## convert suit
			case "h":
				pretty_card = pretty_card + "♥"
			case "d":
				pretty_card = pretty_card + "♦"
			case "s":
				pretty_card = pretty_card + "♠"
			case "c":
				pretty_card = pretty_card + "♣"

		return pretty_card
class Deck:
	SUIT_ORDER = ("d", "h", "c", "s")

	def __init__(self):
		self.cards = []
		self.build()

	def build(self):
		for v in range(2,14):
			for s in self.SUIT_ORDER:
				self.cards.append(Card(v,s))
		self.cards.append(Card(0,'JKR')) ## add Joker into deck
				
	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self, num):
		return [self.cards.pop() for _ in range(0,num)]

	def pretty(self):
		pretty_deck = []
		for card in self.cards:
			pretty_deck.append(card.pretty())
		return pretty_deck

class Hand:
	def __init__(self, cards: list):
		self.cards = cards
	
	def sort(self):
		pass

	def get_outcome(self):
		pass

class Bet:
	def __init__(self, ante: int):
		self.ante = ante

	def add_all(self.__dict__):
		pass

class Player:
	pass

class Dealer:
	pass

class Game:
	pass

bet = Bet(20)
bet.a_high = 1

print(bet.__dict__)