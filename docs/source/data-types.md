# Data Types

**Card** - string

> A three character string that represents card value and suit. Value is represented by the first two character ('02'-'14') and suit is represented by the third character ('s', 'c', 'd', or 'h'). The only exception is the joker which is represented by 'JKR'.
> Example: '12s' represents Q♣ or '14d' represents A♦

**Hand** - list

> A list of cards.
> Example:

```
['02s', '08h', '13c', '05d', '11s']
```

**Bank** - integer

> The total amount the player has to gamble with.
> Example: 1000 represents $1000.00

**Outcome** - dict

> A dictionary that provides game-relevant insight into a hand like poker rank and other possible arrangements.
> Example:

```
outcome = {
    'hand': ['02h', '03h', '05h', '06c', '06s', '13c', '14s'],
    'rank': 'Pair',
    'rank_points': 106.141305,
    'has_joker': False,
    'high_card_order': ['02h', '03h', '05h', '13c', '14s'],
    'multiples': {'06': ['06c', '06s']},
    'multiples_keys': ['06'],
    'straights': [],
    'flushes': [],
    'straight_flushes': [],
    'seven_card_straight_flush': []
}
```

**Rank** - string

> A string that represents a poker rank. All possible examples in order of lowest to highest:

```
'3-A High' ## 'J High' or '9 High'
'Pair'
'Two Pair'
'Three-of-a-kind'
'Straight'
'Flush'
'Full House'
'Straight Flush'
'Royal Flush'
'Five Aces'
'7 Card Straight Flush with Joker'
'Royal Flush Plus Royal Match'
'7 Card Straight Flush, No Joker'
```

**Split** - dict

> A dictionary that represents the two split hand outcomes (high and low) in Pai Gow Poker.
> Example:

```
split = {
    'high': high_outcome,
    'low': low_outcome
}
```

**Bet** or **Winnings** - dict

> A dictionary that represents a player bet on the table or winnings to be returned to the player. Values should be integers to denote the amount. Note: there will always be an ante bet but each game variant might have other bets to play on.
> Example:

```
bet = {
	'ante': 25,
	'ace_high': 5,
	'fortune': 5,
	'progressive': 1,
	'envy': 0
}

winnings = {
	'ante': 50,
	'ace_high': 0,
	'fortune': 0,
	'progressive': 0,
	'envy': 0
}
```

**Result** - string

> A string that represents the result of a game. All possible examples:

```
'Player Wins'
'Dealer Wins'
'Push'
'Push - A High Pai Gow'
```

**Game** - dict

> A dictionary that represents all hands, splits, banks, bets, and winnings in a single game of Pai Gow Poker.
> Example:

```
game = {
	'player_start_bank': 1000,
	'bet': bet,
	'player_hand': player_seven_card_hand,
	'player_split': player_split,
	'dealer_hand': dealer_seven_card_hand,
	'dealer_split': dealer_split,
	'result': 'Player Wins'
	'winnings': winnings,
	'player_end_bank': 1100
}
```

**Session** - pandas.DataFrame

> A dataframe of each game generated from a table.
