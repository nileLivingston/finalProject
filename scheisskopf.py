import game as g

# Main method used for testing.
if __name__ == '__main__':

	wins = [0, 0, 0]
	trials = 1000
	numTurns = []
	printTrials = False
	threshold = 50000
	for i in range(1, trials+1):
		turns = 0
		game = g.Game(False)
		gameBoard = game.getGameBoard()
	
		if printTrials:
			game.printState()
		while not game.isEnded():
			if turns > threshold:
				sys.end()
				break
			game.takeTurn()
			turns += 1
			if printTrials:
				game.printState()
		winner = game.getWinner()
		if winner == None:
			#print "Game " + str(i) + ": Draw"
			wins[0] += 1
		else:
			#print "Game " + str(i) + ": Player " + str(winner)
			wins[winner] += 1
		numTurns.append(turns)

		quintile = trials/5
		if i%quintile == 0:
			print "Experiment progress: " + str((i/(quintile))*20) + "%"

	print "\n"
	print "##############################"
	print "SUMMARY STATISTICS:"
	print "##############################"
	print "Number of games: " + str(trials)
	print "Draw threshold: " + str(threshold)
	print "\n"
	print "Draw rate: " + str(wins[0]/float(trials))
	player1WinRate =  wins[1]/float(trials)
	player2WinRate = wins[2]/float(trials)
	print "Player 1 win rate: " + str(player1WinRate)
	print "Player 2 win rate: " + str(player2WinRate)
	print "\n"
	print "Least number of turns: " + str(min(numTurns))
	print "Greatest number of turns: " + str(max(numTurns))
	print "Average number of turns: " + str(sum(numTurns)/len(numTurns))
	numTurns.sort()
	if trials%2 == 0:
		index = int((float(trials)/2) - 1)
		median = (numTurns[index] + numTurns[index+1])/float(2)
	else:
		index = int((float(trials)/2))
		median = numTurns[index]
	print "Median number of turns: " + str(median)




