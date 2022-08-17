def betting_strat(player_bank:int, last_rank:str, last_outcome:str, last_bet:dict, win_streak:int, loss_streak:int):
	ante = 20 ## ante unit

	## Modified Martingale System
	ladder_top = 8
	second_bonus = 10
	if last_outcome == 'Player Wins':
		ante = ante
	elif last_outcome == 'Dealer Wins' and last_bet:
		if last_bet['ante'] == ante: ## second ladder step
			ante = ante + second_bonus
		else:
			if last_bet['ante'] * 2 < (ante + second_bonus) * 2**(ladder_top-2):
				ante = last_bet['ante'] * 2
			else:
				ante = ante
	elif last_bet:
		ante = last_bet['ante']

	# ## 1-3-2-6 System
	# if last_outcome == 'Player Wins':
	# 	if win_streak%4 == 0:
	# 		ante = ante
	# 	elif win_streak%4 == 1:
	# 		ante = ante * 3
	# 	elif win_streak%4 == 2:
	# 		ante = ante * 2
	# 	elif win_streak%4 == 3:
	# 		ante = ante * 6

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