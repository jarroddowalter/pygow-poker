from cgitb import reset
from itertools import combinations
from unittest import result
import game_configs

DECK = [
'02h', '02d', '02s', '02c',
'03h', '03d', '03s', '03c',
'04h', '04d', '04s', '04c',
'05h', '05d', '05s', '05c',
'06h', '06d', '06s', '06c',
'07h', '07d', '07s', '07c',
'08h', '08d', '08s', '08c',
'09h', '09d', '09s', '09c',
'10h', '10d', '10s', '10c',
'11h', '11d', '11s', '11c',
'12h', '12d', '12s', '12c',
'13h', '13d', '13s', '13c',
'14h', '14d', '14s', '14c',
'JKR'
]

SUIT_ORDER = ['d', 'h', 'c', 's']

def format_card(card:str): ## takes card string and formats for print
	converted_card = ''

	match card[:2]: ## convert num
		case '02':
			converted_card = ' 2'
		case '03':
			converted_card = ' 3'
		case '04':
			converted_card = ' 4'
		case '05':
			converted_card = ' 5'
		case '06':
			converted_card = ' 6'
		case '07':
			converted_card = ' 7'
		case '08':
			converted_card = ' 8'
		case '09':
			converted_card = ' 9'
		case '10':
			converted_card = '10'
		case '11':
			converted_card = ' J'
		case '12':
			converted_card = ' Q'
		case '13':
			converted_card = ' K'
		case '14':
			converted_card = ' A'
		case 'JK':
			converted_card = 'JKR'
	
	match card[-1]: ## convert suit
		case 'h':
			converted_card = converted_card + '♥'
		case 'd':
			converted_card = converted_card + '♦'
		case 's':
			converted_card = converted_card + '♠'
		case 'c':
			converted_card = converted_card + '♣'

	return converted_card

def format_hand(hand): ## takes hand as list and formats for print
	converted_hand = []

	for card in hand:
		converted_hand.append(format_card(card))

	return converted_hand

def sort_hand(hand): ## takes preformatted hand
	global SUIT_ORDER
	result = list(hand)
	if len(result) == 1:
		return result
	else:
		result.sort()

	def get_card_suit_order(card:str):
		if card == "JKR":
			return 4 ## returns index of suit order
		for i, suit in enumerate(SUIT_ORDER):
			if card[-1] == suit:
				return i

	i = 1
	while i < len(result):
		if result[i][:2] == result[i-1][:2] and get_card_suit_order(result[i]) < get_card_suit_order(result[i-1]):
			result.insert(i-1, result.pop(i))
			i = 1
		else:
			i += 1
	
	return result

def read_hand(hand): ## returns outcome as a dict
	sorted_hand = sort_hand(hand)
	outcome = {
		'hand': sort_hand(hand),				## sorted hand by rank as list
		'rank': '',							## rank as string
		'rank_points': 0,					## rank points as int
		'has_joker': False,					## joker in hand as bool
		'high_card_order': [],				## list of high cards in hand in ascending order
		'multiples': {},					## dict of multiples as a list of cards; keys are card value
		'multiples_keys': [],				## list of keys for multiples
		'straights': [], 					## lists of lists of possible straight hands	
		'flushes': [],						## lists of lists of possible flush hands		
		'straight_flushes': [],				## list of lists of possible straight flush hands
		'seven_card_straight_flush': []		## list of cards in seven card straight flush
	}

	## count num and suits
	num_count = {}
	suit_count = {}

	for card in sorted_hand:
		if card == "JKR":
			outcome['has_joker'] = True
			if num_count.get('14', False): 
				num_count['14'] += 1
			else:
				num_count['14'] = 1
		else:
			if num_count.get(card[:2], False): 
				num_count[card[:2]] += 1
			else:
				num_count[card[:2]] = 1
			if suit_count.get(card[-1], False):
				suit_count[card[-1]] += 1
			else:
				suit_count[card[-1]] = 1

	## get high card order
	for key, val in num_count.items():
		if key == '14' and val == 1 and outcome['has_joker']:
			outcome['high_card_order'].append('JKR')
		elif val == 1:
			for card in sorted_hand:
				if card[:2] == key:
					outcome['high_card_order'].append(card)
	
	## get multiples
	for key, val in num_count.items():
		if key != '14' and val > 1:
			outcome['multiples'][key] = []
			for card in sorted_hand:
				if card[:2] == key:
					outcome['multiples'][key].append(card)
		elif key == '14' and val > 1:
			outcome['multiples'][key] = []
			for card in sorted_hand:
				if card[:2] == key or card == 'JKR':
					outcome['multiples'][key].append(card)

	outcome['multiples_keys'] = list(outcome['multiples'].keys())

	## get straights
	possible_five_card_hands = list(combinations(sorted_hand, 5))

	for h in possible_five_card_hands:
		list_hand = list(h)
		result = []
		joker_in_hand = False
		if 'JKR' in list_hand:
			list_hand.pop(list_hand.index('JKR'))
			joker_in_hand = True
		ace = ''
		for card in list_hand:
			if card[:2] == '14':
				ace = card
				list_hand.pop(list_hand.index(ace))

		for i, card in enumerate(list_hand):
			if i == 0 and card[:2] == '02':
				if ace:
					result.append(ace)
					result.append(card)
				elif joker_in_hand:
					result.append('JKR')
					result.append(card)
				else:
					result.append(card)
			elif i == 0 and card[:2] == '03':
				if ace and joker_in_hand:
					result.append(ace)
					result.append('JKR')
					result.append(card)
				else:
					result.append(card)
			elif i == 0:
				if joker_in_hand:
					result.append('JKR')
					result.append(card)
				else:
					result.append(card)
			elif int(card[:2]) - 1 == int(result[-1][:2]):
				result.append(card)
			elif joker_in_hand and int(card[:2]) - 2 == int(result[-1][:2]):
				if 'JKR' in result:
					result = result[result.index('JKR')+1:]
				result.append('JKR')
				result.append(card)
			else:
				break

		if result[-1][:2] == '13' or (result[-1] == 'JKR' and result[-2][:2] == '12'):
			if ace:
				result.append(ace)
		
		if len(result) == 5:
			outcome['straights'].append(result)
			if result[0] == 'JKR' and result[-1][:2] != '14':
				outcome['straights'].append([result[1], result[2], result[3], result[4], 'JKR'])
			
	## get flushes
	flush_cards = []
	for key, val in suit_count.items():
		if val >= 5 or (val == 4 and outcome['has_joker']):
			for card in sorted_hand:
				if card[-1] == key or card == 'JKR':
					flush_cards.append(card)

	if len(flush_cards) >= 5:
		outcome['flushes'] += list(combinations(flush_cards, 5))

	## get straight flushes
	if outcome['straights'] and outcome['flushes']:
		for h in outcome['straights']:
			for i, card in enumerate(h):
				if card[-1] == outcome['flushes'][0][0][-1] or card == 'JKR':
					if i == 4:
						outcome['straight_flushes'].append(h)
					else:
						continue
				else:
					break

	## get seven card straight flush
	if outcome['straight_flushes']:
		list_hand = sorted_hand
		result = []
		joker_in_hand = False
		if 'JKR' in list_hand:
			list_hand.pop(list_hand.index('JKR'))
			joker_in_hand = True
		ace = ''
		for card in list_hand:
			if card[:2] == '14':
				ace = card
				list_hand.pop(list_hand.index(ace))

		for i, card in enumerate(list_hand):
			if i == 0 and card[:2] == '02':
				if ace:
					result.append(ace)
					result.append(card)
				elif joker_in_hand:
					result.append('JKR')
					result.append(card)
				else:
					result.append(card)
			elif i == 0 and card[:2] == '03':
				if ace and joker_in_hand:
					result.append(ace)
					result.append('JKR')
					result.append(card)
				else:
					result.append(card)
			elif i == 0:
				if joker_in_hand:
					result.append('JKR')
					result.append(card)
				else:
					result.append(card)
			elif int(card[:2]) - 1 == int(result[-1][:2]):
				result.append(card)
			elif joker_in_hand and int(card[:2]) - 2 == int(result[-1][:2]):
				if 'JKR' in result:
					result = result[result.index('JKR')+1:]
				result.append('JKR')
				result.append(card)
			else:
				break

		if result[-1][:2] == '13' or ((result[-1] == 'JKR' and result[-2][:2] == '12')):
			if ace:
				result.append(ace)

		if result[0] == 'JKR' and result[-1][:2] != '14':
			result = result[1:]
			result.append('JKR')

		has_flush = True
		for card in result:
			if card[-1] == outcome['flushes'][0][0][-1] or card == 'JKR':
				continue
			else:
				has_flush = False
				break
		
		if len(result) == 7 and has_flush:
			outcome['seven_card_straight_flush'] = result
	
	#### Score Hand ####

	## 7 Card Straight Flush, No Joker		30000 + 1-8 straight rank (8-9-10-J-Q-K-A highest)
	if len(hand) == 7 and outcome['seven_card_straight_flush'] and not outcome['has_joker']:
		outcome['rank'] = '7 Card Straight Flush, No Joker'
		if outcome['seven_card_straight_flush'][0][:2] == '14':
			outcome['rank_points'] = 30001
		else:
			outcome['rank_points'] = 30000 + int(outcome['straight_flush'][0][:2])
		return outcome

	## Royal Flush Plus Royal Match			20000 + 1-2 royal match rank (A-K > K-Q of same suite/no joker)
	if len(hand) == 7 and outcome['straight_flushes'] and (outcome['straight_flushes'][-1][0][:2] == '10' or (outcome['straight_flushes'][-1][0] == 'JKR' and outcome['straight_flushes'][-1][1][:2] == '11')):
		r_flush = outcome['straight_flushes'][-1]
		r_match = []
		for card in hand:
			if card not in r_flush:
				r_match.append(card)
		print(r_match)
		# if r_match[0][-1] == r_match[1][-1] and r_match[0][:2] == '13' and r_match[1][:2] == '14': ## some sources say A K pair counts as a royal match and some don't
		# 	outcome['rank'] = 'Royal Flush Plus Royal Match'
		# 	outcome['rank_points'] = 20000 + 1
		# 	return outcome
		if r_match[0][-1] == r_match[1][-1] and r_match[0][:2] == '12' and r_match[1][:2] == '13': ## check Q K suit match
			outcome['rank'] = 'Royal Flush Plus Royal Match'
			outcome['rank_points'] = 20000
			return outcome

	## 7 Card Straight Flush with Joker		10000 + 1-8 straight rank (8-9-10-J-Q-K-A highest)
	if len(hand) == 7 and outcome['seven_card_straight_flush'] and outcome['has_joker']:
		outcome['rank'] = '7 Card Straight Flush with Joker'
		if outcome['seven_card_straight_flush'][0][:2] == '14':
			outcome['rank_points'] = 10000 + 1
		elif outcome['seven_card_straight_flush'][0] == 'JKR' and outcome['seven_card_straight_flush'][1][:2] == '09':
			outcome['rank_points'] = 10000 + 8
		else:
			outcome['rank_points'] = 10000 + int(outcome['seven_card_straight_flush'][0][:2])
		return outcome

	## Five Aces							9000
	if '14' in outcome['multiples'] and outcome['multiples']['14'] == 5:
		outcome['rank'] = 'Five Aces'
		outcome['rank_points'] = 9000
		return outcome

	## Royal Flush							8000
	if outcome['straight_flushes'] and (outcome['straight_flushes'][-1][0][:2] == '10' or (outcome['straight_flushes'][-1][0] == 'JKR' and outcome['straight_flushes'][-1][1][:2] == '11')):
		outcome['rank'] = 'Royal Flush'
		outcome['rank_points'] = 8000

		if len(hand) == 5: ## sort hand by royal flush
			outcome['hand'] = outcome['straight_flushes'][-1]
		return outcome

	## Straight Flush						7000 + 2-10 straight rank (A-2-3-4-5 highest)
	if outcome['straight_flushes']:
		outcome['rank'] = 'Straight Flush'
		if outcome['straight_flushes'][0][0][:2] == '14' or outcome['straight_flushes'][0][0] == 'JKR':
			outcome['rank_points'] = 7000 + 10
		else:
			outcome['rank_points'] = 7000 + int(outcome['straight_flushes'][-1][-5][:2])

		if len(hand) == 5: ## sort hand by straight flush
			outcome['hand'] = outcome['straight_flushes'][-1]
		return outcome

	## Four-of-a-kind						6000 + 2-14 card val
	for key in outcome['multiples_keys']:
		if len(outcome['multiples'][key]) == 4:
			outcome['rank'] = 'Four-of-a-kind'
			outcome['rank_points'] = 6000 + int(key)
			return outcome

	## Full House							5000 + 2-14 three-of-a-kind card val
	three_key = ''
	two_key = ''
	for key in outcome['multiples_keys']:
		if len(outcome['multiples'][key]) == 3:
			if three_key:
				two_key = three_key
				three_key = key
			else:
				three_key = key
		elif len(outcome['multiples'][key]) == 2:
			two_key = key
	if three_key and two_key:
		outcome['rank'] = 'Full House'
		outcome['rank_points'] = 5000 + int(three_key)
		return outcome

	## Flush								4000 + 6-14 highest card in flush val
	if outcome['flushes']:
		outcome['rank'] = 'Flush'
		if outcome['flushes'][-1][-1] == 'JKR':
			outcome['rank_points'] = 7000 + 140
		else:
			outcome['rank_points'] = 7000 + int(outcome['flushes'][-1][-1][:2])*10
		return outcome

	## Straight								3000 + 1-10 straight rank (10-J-Q-K-A highest)
	if outcome['straights']:
		outcome['rank'] = 'Straight'
		if outcome['straights'][-1][0][:2] == '14' or (outcome['straights'][-1][-5] == 'JKR' and outcome['straights'][-1][-4][:2] == '02'):
			outcome['rank_points'] = 3000 + 1
		elif outcome['straights'][-1][-5] == 'JKR' and outcome['straights'][-1][-1][:2] == '14':
			outcome['rank_points'] = 3000 + 10
		else:
			outcome['rank_points'] = 3000 + int(outcome['straights'][-1][-5][:2])

		if len(hand) == 5: ## sort hand by straight
			outcome['hand'] = outcome['straights'][-1]
		return outcome

	## Three-of-a-kind						2000 + 2-14 card val
	if len(outcome['multiples_keys']) == 1 and len(outcome['multiples'][outcome['multiples_keys'][0]]) == 3:
		outcome['rank'] = 'Three-of-a-kind'
		outcome['rank_points'] = 2000 + int(outcome['multiples_keys'][0])
		return outcome

	## Two Pair								1000 + 2-14 high pair card val
	if len(outcome['multiples_keys']) >= 2 and len(outcome['multiples'][outcome['multiples_keys'][-1]]) == 2 and len(outcome['multiples'][outcome['multiples_keys'][-2]]) == 2:
		outcome['rank'] = 'Two Pair'
		high_card_points = 0
		if outcome['high_card_order'][-1] == 'JKR':
			high_card_points = 14/10000
		else:
			high_card_points = int(outcome['high_card_order'][-1][:2])/10000
		outcome['rank_points'] = 1000 + int(outcome['multiples_keys'][-1]) + int(outcome['multiples_keys'][-2])/100 + high_card_points
		return outcome

	## Pair									100 + 2-14 card val
	if len(outcome['multiples_keys']) == 1 and len(outcome['multiples'][outcome['multiples_keys'][0]]) == 2:
		outcome['rank'] = 'Pair'
		high_card_one_points = 0
		high_card_two_points = 0
		high_card_three_points = 0
		if len(outcome['high_card_order']) >= 3:
			if outcome['high_card_order'][-1] == 'JKR':
				high_card_one_points = 14/100
				high_card_two_points = int(outcome['high_card_order'][-2][:2])/10000
				high_card_three_points = int(outcome['high_card_order'][-3][:2])/1000000
			else:
				high_card_one_points = int(outcome['high_card_order'][-1][:2])/100
				high_card_two_points = int(outcome['high_card_order'][-2][:2])/10000
				high_card_three_points = int(outcome['high_card_order'][-3][:2])/1000000
		outcome['rank_points'] = 100 + int(outcome['multiples_keys'][-1]) + high_card_one_points + high_card_two_points + high_card_three_points
		return outcome

	## High									2-14 card val
	if outcome['high_card_order']:
		if outcome['high_card_order'][-1] == 'JKR' or outcome['high_card_order'][-1][:2] == '14':
			outcome['rank'] = 'A High'
		elif outcome['high_card_order'][-1][:2] == '13':
			outcome['rank'] = 'K High'
		elif outcome['high_card_order'][-1][:2] == '12':
			outcome['rank'] = 'Q High'
		elif outcome['high_card_order'][-1][:2] == '11':
			outcome['rank'] = 'J High'
		else:
			outcome['rank'] = str(int(outcome['high_card_order'][-1][:2])) + ' High'

		high_card_one_points = 0
		high_card_two_points = 0
		high_card_three_points = 0
		high_card_four_points = 0

		if len(outcome['high_card_order']) >= 5:
			high_card_one_points = int(outcome['high_card_order'][-2][:2])/100
			high_card_two_points = int(outcome['high_card_order'][-3][:2])/10000
			high_card_three_points = int(outcome['high_card_order'][-4][:2])/1000000
			high_card_four_points = int(outcome['high_card_order'][-5][:2])/100000000
		elif len(outcome['high_card_order']) == 2:
			high_card_one_points = int(outcome['high_card_order'][-2][:2])/100

		if outcome['high_card_order'][-1] == 'JKR':
			outcome['rank_points'] = 14 + high_card_one_points + high_card_two_points + high_card_three_points + high_card_four_points
		else:
			outcome['rank_points'] = int(outcome['high_card_order'][-1][:2]) + high_card_one_points + high_card_two_points + high_card_three_points + high_card_four_points
		return outcome

## helper function removes cards of one hand from the other; returns new hand
def subtract_hand(hand:list, subtract_hand:list):
	result = list(hand)
	i = 0
	while i < len(result):
		if result[i] in subtract_hand:
			result.pop(i)
			i = 0
		else:
			i += 1
	return result

def custom_split(high_hand:list, low_hand:list): ## takes a high hand list and a low hand list and returns a split dict
	split = {
		'high': {},
		'low': {},
	}

	## check if high hand is 5 cards, low hand is 2 cards
	## check if outcome of 5 card hand is better than outcome of 2 card hand

	## use outcome of 7 cards to determine split

	## move correct cards to split dict

	##	get outcomes of both hands

	return split

def determine_winner(player_split:dict, dealer_split:dict):
	if dealer_split['high']['rank'] == 'A High': ## Push on A High Pai Gow
		return 'Push - A High Pai Gow'
	elif player_split['high']['rank_points'] > dealer_split['high']['rank_points'] and player_split['low']['rank_points'] > dealer_split['low']['rank_points']:
		return 'Player Wins'
	elif player_split['high']['rank_points'] > dealer_split['high']['rank_points'] or player_split['low']['rank_points'] > dealer_split['low']['rank_points']:
		return 'Push'
	else:
		return 'Dealer Wins'

def add_bet(bet:dict): ## add bet or total winnings
	result = bet['ante'] + bet['ace_high'] + bet['fortune'] + bet['progressive'] + bet['envy']
	return result

def determine_winnings(bet:dict, outcome:str, rank:str, dealer_rank:str, dealer_hand:list):
	winnings = {
		'ante': 0,
		'ace_high': 0,
		'fortune': 0,
		'progressive': 0,
		'envy': 0
	}

	## ante
	if outcome == 'Player Wins':
		winnings['ante'] = bet['ante'] * 2
	elif outcome == 'Dealer Wins':
		winnings['ante'] = 0
	else: ## push
		winnings['ante'] = bet['ante']

	## ace high
	if dealer_rank == 'A High' and 'JKR' not in dealer_hand:
		if type(game_configs.ACE_HIGH_PAYOUT['Dealer A High No Joker']) == int:
			winnings['ace_high'] = bet['ace_high'] * game_configs.ACE_HIGH_PAYOUT['Dealer A High No Joker']
		elif type(game_configs.ACE_HIGH_PAYOUT['Dealer A High No Joker']) == str:
			winnings['ace_high'] = bet['ace_high'] + int(game_configs.ACE_HIGH_PAYOUT['Dealer A High No Joker'])
	elif dealer_rank == 'A High' and 'JKR' in dealer_hand:
		if type(game_configs.ACE_HIGH_PAYOUT['Dealer A High with Joker']) == int:
			winnings['ace_high'] = bet['ace_high'] * game_configs.ACE_HIGH_PAYOUT['Dealer A High with Joker']
		elif type(game_configs.ACE_HIGH_PAYOUT['Dealer A High with Joker']) == str:
			winnings['ace_high'] = bet['ace_high'] + int(game_configs.ACE_HIGH_PAYOUT['Dealer A High with Joker'])
	elif rank == 'A High' and dealer_rank == 'A High':
		if type(game_configs.ACE_HIGH_PAYOUT['Dealer and Player A High']) == int:
			winnings['ace_high'] = bet['ace_high'] * game_configs.ACE_HIGH_PAYOUT['Dealer and Player A High']
		elif type(game_configs.ACE_HIGH_PAYOUT['Dealer and Player A High']) == str:
			winnings['ace_high'] = bet['ace_high'] + int(game_configs.ACE_HIGH_PAYOUT['Dealer and Player A High'])

	## fortune
	if rank in game_configs.FORTUNE_BONUS_PAYOUT:
		if type(game_configs.FORTUNE_BONUS_PAYOUT[rank]) == int:
			winnings['fortune'] = bet['fortune'] * game_configs.FORTUNE_BONUS_PAYOUT[rank]
		elif type(game_configs.FORTUNE_BONUS_PAYOUT[rank]) == str:
			winnings['fortune'] = bet['fortune'] + int(game_configs.FORTUNE_BONUS_PAYOUT[rank])

	## progressive
	if rank in game_configs.PROGRESSIVE_BONUS_PAYOUT:
		if type(game_configs.PROGRESSIVE_BONUS_PAYOUT[rank]) == int:
			winnings['progressive'] = bet['progressive'] * game_configs.PROGRESSIVE_BONUS_PAYOUT[rank]
		elif type(game_configs.PROGRESSIVE_BONUS_PAYOUT[rank]) == str:
			winnings['progressive'] = bet['progressive'] + int(game_configs.PROGRESSIVE_BONUS_PAYOUT[rank])

	## envy - not setup yet


	return winnings

def sort_dict(d:dict):
	result = {}
	for key in sorted(d.keys()):
		result[key] = d[key]
	return result