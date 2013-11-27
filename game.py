import random
import GameBoard as gb
import util
import agents

# Represents an instance of a Scheisskopf game. Handles all control related to
# turn-taking and GameBoard manipulation.
class Game:

	# Construct players and GameBoard.
	def __init__(self, playerOneHuman):
		self.inPregame = True
		self.playerOne = agents.GreedyAgent(1)
		self.playerTwo = agents.RandomAgent(2)
		self.players = [self.playerOne, self.playerTwo]

		self.gameBoard = gb.GameBoard(self.players)
		self.activePlayer = random.choice(self.players)
		self.pileCard = None
		self.ended = False
		self.winner = None

	#######################################################
	#######################################################
	# PRINT METHOD:
	#######################################################
	#######################################################

	# Prints the current state of the game.
	def printState(self):
		print self.gameBoard.deckToString()
		print self.gameBoard.handsToString()
		print self.gameBoard.upCardsToString()
		print self.gameBoard.downCardsToString()
		print self.gameBoard.pileToString()
		print self.gameBoard.discardToString()
		print "Active player: " + str(self.activePlayer.getID())
		print "HeuristicAgent's Representations:"
		print "Opp hand: "
		#print self.playerTwo.oppHandRepToString()
		print "Pile:"
		#print self.playerTwo.pileRepToString()
		print "Discard:"
		#print self.playerTwo.discardRepToString()
		print "\n"

	#######################################################
	#######################################################
	# ACCESSOR METHODS:
	#######################################################
	#######################################################	

	# Returns the GameBoard.
	def getGameBoard(self):
		return self.gameBoard

	# Returns the ID of the active player.
	def getActivePlayer(self):
		return self.activePlayer.getID()

	# Returns the winner of the game.
	def getWinner(self):
		return self.winner

	# True iff game is over.
	def isEnded(self):
		return self.ended

	#######################################################
	#######################################################
	# MUTATOR METHODS:
	#######################################################
	#######################################################

	# Moves the game forward a single turn and change activePlayer.
	def takeTurn(self):
		# Check to see if the game is ended.
		if self.gameBoard.isTerminal():
			self.ended = True
			self.changeActivePlayer()
			self.winner = self.activePlayer.getID()	
			return

		# Look at the card on top of the pile.
		self.pileCard = self.gameBoard.peekPile()
		
		# If there's a ten on the pile, clear and skip activePlayer's turn.
		if not self.pileCard == None and (self.pileCard.getRank() == 10 or self.gameBoard.topFourSame()):
			self.gameBoard.clearPile()
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("DISCARD")
			self.changeActivePlayer()
			return

		# If there's a three on the pile, discard the three, force activePlayer to
		# pick up pile and skip their turn.
		if not self.pileCard == None and self.pileCard.getRank() == 3:
			self.gameBoard.clearTopCard()
			self.gameBoard.pileToHand(self.activePlayer)
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("PICKUP", self.activePlayer.getID())
			self.changeActivePlayer()
			return

		# If we're in the pregame, prompt swap from activePlayer.
		if self.inPregame:
			self.swapPlay()

		# If we're doing normal turn taking, make activePlayer take a turn.	
		else:
			# Down cards are available for player. No need to actually choose; random anyway.
			if self.gameBoard.downCardsPlayable(self.activePlayer.getID()):
				self.downCardPlay()

			# Up cards are available for player.
			elif self.gameBoard.upCardsPlayable(self.activePlayer.getID()):
				self.upCardPlay()

			# Player still has a hand to play.
			else:
				self.handCardsPlay()

	# Hand over turn-taking control.
	def changeActivePlayer(self):
		# Hand over turn-taking control.
		if self.activePlayer == self.playerOne:
			self.activePlayer = self.playerTwo
		elif self.activePlayer == self.playerTwo:
			self.activePlayer = self.playerOne

	# Handles a swap.
	def swapPlay(self):
		hand = self.gameBoard.viewHand(self.activePlayer)
		upCards = self.gameBoard.viewUpCards(self.activePlayer)
		playableCards = self.gameBoard.getPlayableHandCards(self.activePlayer)
		swap = self.activePlayer.chooseSwap(hand, upCards, playableCards)
		upCard = swap[0]
		handCards = swap[1]
		# Check to see if swap is actually a request to play.
		# If so, submit that action.
		if upCard == None:
			self.handCardsPlay(handCards)
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("PLAY", self.activePlayer.getID(), handCards)
			self.inPregame = False
			#self.changeActivePlayer()
			return

		# Check legality of swap and apply if legal.
		else:
			if self.gameBoard.isLegalSwap(upCard, handCards, self.activePlayer):
				self.gameBoard.applySwap(swap, self.activePlayer)
				self.changeActivePlayer()
				# Send percepts to all players.
				for player in self.players:
					player.updateKnowledge("SWAP", self.activePlayer.getID(), upCard, handCards)
						

	# Handles the playing of a down card.
	def downCardPlay(self):
		# Select a down card and put it on the pile.
		self.activePlayer.chooseDownCard()	
		numDownCards = len(self.gameBoard.viewDownCards(self.activePlayer))
		indexList = []
		for i in range(0, numDownCards):
			indexList.append(i)
		index = random.choice(indexList)
		downCard = self.gameBoard.viewDownCards(self.activePlayer).pop(index)
		self.gameBoard.downCardToPile(self.activePlayer, downCard)
		# Send percepts to all players.
		for player in self.players:
			player.updateKnowledge("PLAY", self.activePlayer.getID(), [downCard])
				
		# If the card is not playable on the pile, pick it all up.
		if not downCard.isPlayableOn(self.pileCard):
			self.gameBoard.pileToHand(self.activePlayer)
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("PICKUP", self.activePlayer.getID())
		self.changeActivePlayer()

	# Handles the playing of an up card.
	def upCardPlay(self):
		upCards = self.gameBoard.viewUpCards(self.activePlayer)
		playableCards = self.gameBoard.getPlayableUpCards(self.activePlayer)
		action = self.activePlayer.chooseUpCard(upCards, playableCards)
		# Make sure a null action is true. If so, pick up pile.
		if action == []:
			if playableCards == []:
				self.gameBoard.pileToHand(self.activePlayer)
				# Send percepts to all players.
				for player in self.players:
					player.updateKnowledge("PICKUP", self.activePlayer.getID())
				self.changeActivePlayer()
				return
			else:
				return

		# Check to see if action is valid. If so, play cards.
		if self.gameBoard.isLegalUpCardPlay(action, self.activePlayer):
			self.gameBoard.upCardsToPile(self.activePlayer, action)
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("PLAY", self.activePlayer.getID(), action)
			self.changeActivePlayer()
			return

	# Handles the playing of hand cards.
	def handCardsPlay(self, action=None):
		hand = self.gameBoard.viewHand(self.activePlayer)
		upCards = self.gameBoard.viewUpCards(self.activePlayer)
		playableCards = self.gameBoard.getPlayableHandCards(self.activePlayer)

		if action == None:	
			action = self.activePlayer.chooseHandCard(hand, upCards, playableCards)
		# Make sure a null action is true. If so, pick up the pile.
		if action == []:
			if playableCards == []:
				self.gameBoard.pileToHand(self.activePlayer)
				# Send percepts to all players.
				for player in self.players:
					player.updateKnowledge("PICKUP", self.activePlayer.getID())
				self.changeActivePlayer()
				return
			else:
				print "ILLEGAL []"
				return

		# Check to see if action is valid. If so, play cards.
		if self.gameBoard.isLegalHandCardPlay(action, self.activePlayer):
			self.gameBoard.handToPile(self.activePlayer, action)
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("PLAY", self.activePlayer.getID(), action)
			self.changeActivePlayer()
			return
		else:
			print "ILLEGAL MOVE"