import game as g

class Experiment:

	def __init__(self, trials, playerOneType, playerTwoType):
		self.trials = trials
		self.playerOneType = playerOneType
		self.playerTwoType = playerTwoType

	def run(self):
		wins = [0, 0, 0]
		numTurns = []
		printTrials = False
		threshold = 5000

		print "\n"
		print "##############################"
		print "RUNNING EXPERIMENT: " + self.playerOneType + " vs. " + self.playerTwoType
		print "Number of trials: " + str(self.trials)
		print "Draw threshold: " + str(threshold)
		print "##############################"
		print "\n"
		for i in range(1, self.trials+1):
			turns = 0
			game = g.Game(self.playerOneType, self.playerTwoType)
			gameBoard = game.getGameBoard()
		
			if printTrials:
				game.printState()
			while not game.isEnded():
				if turns > threshold:
					#sys.end()
					break
				game.takeTurn()
				turns += 1
				if printTrials:
					game.printState()
			winner = game.getWinner()
			if winner == None:
				wins[0] += 1
			else:
				wins[winner] += 1
			numTurns.append(turns)

			if self.trials > i:
				tenth = self.trials/10
				if i%tenth == 0:
					print "Experiment progress: " + str((i/(tenth))*10) + "%"

		print "\n"
		print "##############################"
		print "SUMMARY STATISTICS:"
		print "##############################"
		print "Draw rate: " + str(wins[0]/float(self.trials))
		player1WinRate =  wins[1]/float(self.trials)
		player2WinRate = wins[2]/float(self.trials)
		print "Player 1 (" + self.playerOneType + ") win rate: " + str(player1WinRate)
		print "Player 2 (" + self.playerTwoType + ") win rate: " + str(player2WinRate)
		print "\n"
		print "Least number of turns: " + str(min(numTurns))
		print "Greatest number of turns: " + str(max(numTurns))
		print "Average number of turns: " + str(sum(numTurns)/len(numTurns))
		numTurns.sort()
		if self.trials%2 == 0:
			index = int((float(self.trials)/2) - 1)
			median = (numTurns[index] + numTurns[index+1])/float(2)
		else:
			index = int((float(self.trials)/2))
			median = numTurns[index]
		print "Median number of turns: " + str(median)