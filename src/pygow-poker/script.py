import random
from typing import Union

class Card:
	def __init__(self, value: int, suit: str):
		self._value = value
		self._suit = suit

	@property
	def value(self):
		return self._value

	@property
	def suit(self):
		return self._suit

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
		self._cards = []
		self.build()

	@property
	def cards(self):
		return self._cards

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
	def __init__(self, cards: Union[object, list]):
		self.validate_cards(cards)
		self._cards = cards

	@property
	def cards(self):
		return self._cards
	
	def sort(self):
		pass
		# result = list(hand)
		# if len(result) == 1:
		# 	return result
		# else:
		# 	result.sort()

		# def get_card_suit_order(card: str):
		# 	if card == "JKR":
		# 		return 4  ## returns index of suit order
		# 	for i, suit in enumerate(Deck.SUIT_ORDER):
		# 		if card[-1] == suit:
		# 			return i

		# i = 1
		# while i < len(result):
		# 	if result[i][:2] == result[i - 1][:2] and get_card_suit_order(
		# 		result[i]
		# 	) < get_card_suit_order(result[i - 1]):
		# 		result.insert(i - 1, result.pop(i))
		# 		i = 1
		# 	else:
		# 		i += 1

		 

		# i = 0
		# while i < len(self.cards):
		# 	if cards[i]

	def add(self, to_add: Union[object, list]):
		self.validate_cards(to_add)

		if isinstance(to_add, Card):
			self.cards.append(to_add)
		else:
			self.cards.extend(to_add)
			

	def subtract(self, to_subtract: Union[object, list]):
		result = self.validate_cards(to_subtract)

		# i = 0
		# while i < len(self.cards):
		# 	if self.cards[i] in ts:
		# 		self.cards.pop(i)
		# 		i = 0
		# 	else:
		# 		i += 1

	def get_outcome(self):
		pass

	def pretty(self):
		pretty_hand = []
		for card in self.cards:
			pretty_hand.append(card.pretty())
		return pretty_hand

	def validate_cards(self, cards: Union[object, list]):
		result = []
		if type(cards) == object and not isinstance(cards, Card):
			raise TypeError("Error: Object not instance of Card.")
		elif type(cards) == list:
			for card in cards:
				if not isinstance(card, Card):
					raise TypeError("Error: Items in list are not instances of Card.")

		if type(cards) == object:
			result = [cards]

		return result
class Bet:
	def __init__(self, ante: int):
		self.ante = ante

	def add_all(self):
		pass

class Player:
	pass

class Dealer:
	pass

class Game:
	pass

c1 = Card(2, 's')
c2 = Card(3, 'd')
c3 = Card(4, 'h')
c4 = Card(5, 'c')

h1 = Hand(c3)
h1.subtract(c3)
print(h1.pretty())
