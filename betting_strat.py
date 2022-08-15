def betting_strat(player_bank:int, last_rank:str, last_outcome:str, last_bet:dict):
	ante = 15 ## lowest ante on ladder

	if last_outcome == 'Player Wins':
		ante = 15
	elif last_outcome == 'Dealer Wins' and last_bet:
		if last_bet == 15:
			ante = 20
		else:
			ante = last_bet['ante'] * 2
	elif last_bet:
		ante = last_bet['ante']

	ace_high = 0
	fortune = 0
	progressive = 0 ## max of 1
	envy = 0 ## don't have multiple seat games setup yet

	bet = {
		'ante': ante,
		'ace_high': ace_high,
		'fortune': fortune,
		'progressive': progressive,
		'envy': envy
	}

	return bet