import util
import random

#######################################################
#######################################################
# agents.py
#
# This file contains all of our Agent classes
# At the beginning is an "abstract" Agent class, used
# to specify all of the necessary methods for a functional
# Agent.
#######################################################
#######################################################

# Abstract description of a Schiesskopf agent.
class Agent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.type = "ABSTRACTAGENT"

	def getID(self):
		return self.agentID

	def getType(self):
		return self.type

	# Returns a list of playable hand cards.
	def chooseHandCard(self, hand, upCards, playableCards):
		return 

	# Returns a list of playable up cards.
	def chooseUpCard(self, upCards, playableCards):
		return

	# Trivial method. Computer agents always just return,
	# HumanAgent will be prompted by chooseDownCard for input.
	# Because no choice is necessary with down cards, this is purely
	# an input verification method.
	def chooseDownCard(self):
		return

	# Returns a double indicating a swap: (upCard, handCard).
	def chooseSwap(self, hand, upCards, playableCards):
		return

	# Used to update knowledge representations for Agents that use them.
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		return


# An agent that chooses actions randomly.
class RandomAgent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.type = "RandomAgent"

	def getID(self):
		return self.agentID

	def getType(self):
		return self.type

	# Randomly chooses a legal action.
	def chooseHandCard(self, hand, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			rank = random.choice(playableCards).getRank()
			#cardsToPlay = self.getAllOfRank(rank, playableCards)
			cardsToPlay = self.getSomeOfRank(rank, playableCards)
			return cardsToPlay

	# Choose legal up card(s) to play.
	def chooseUpCard(self, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			rank = random.choice(playableCards).getRank()
			#cardsToPlay = self.getAllOfRank(rank, playableCards)
			cardsToPlay = self.getSomeOfRank(rank, playableCards)
			return cardsToPlay

	def chooseDownCard(self):
		return

	# Randomly chooses a legal swap or to begin turn-taking.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return (None, cardList).
	def chooseSwap(self, hand, upCards, playableCards):
		# Randomly choose between swapping and putting down.
		if random.choice([0, 1]) == 1:
			# Return a valid first play.
			handPlay = [random.choice(hand)]
			return (None, handPlay)
		
		else:
			# Return a valid swap.
			upSwap = random.choice(upCards)
			handSwap = random.choice(hand)
			return (upSwap, handSwap)

	# No knowledge is stored, so method is trivial.
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		return

	#######################################################
	#######################################################
	# HELPER METHODS
	#######################################################
	#######################################################

	# Return a list of all cards in playableCards of a certain rank.
	def getAllOfRank(self, rank, playableCards):
		output = []
		for card in playableCards:
			if card.getRank() == rank:
				output.append(card)
		return output

	# Return a list of cards in playableCards of a certain rank.
	# Must return at least one card.
	def getSomeOfRank(self, rank, playableCards):
		output = []
		pickedOne = False
		for card in playableCards:
			if not pickedOne and card.getRank() == rank:
				output.append(card)
			elif pickedOne and card.getRank() == rank:
				choice = random.choice([0, 1])
				if choice == 1:
					output.append(card)
		return output

# An Agent that plays all cards of the lowest-valued playable rank it has.
class GreedyAgent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.type = "GreedyAgent"

	def getID(self):
		return self.agentID

	def getType(self):
		return self.type

	# Choose all cards of the lowest playable rank in hand.
	def chooseHandCard(self, hand, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			return self.worstCardsInList(playableCards)

	# Choose all cards of the lowest playable rank in upCards.
	def chooseUpCard(self, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			return self.worstCardsInList(playableCards)

	def chooseDownCard(self):
		return

	# Swap best card in hand with worst card in up cards until
	# there are no more productive swaps.
	def chooseSwap(self, hand, upCards, playableCards):
		bestHandCard = self.bestCardInList(hand)
		worstUpCard = self.worstCardInList(upCards)
		# If there are no more productive swaps, play lowest card(s).
		if not bestHandCard.isBetterThan(worstUpCard):
			worstHandCards = self.worstCardsInList(playableCards)
			return (None, worstHandCards)
		
		# Return a valid swap.
		else:
			return (worstUpCard, bestHandCard)

	# No knowledge is stored, so method is trivial.
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		return

	#######################################################
	#######################################################
	# HELPER METHODS
	#######################################################
	#######################################################

	# Return one of the best cards in a list.
	def bestCardInList(self, cardList):
		bestCard = cardList[0]
		for card in cardList:
			if card.isBetterThan(bestCard):
				bestCard = card
		return bestCard

	# Return one of the worst cards in a list.
	def worstCardInList(self, cardList):
		worstCard = cardList[0]
		for card in cardList:
			if worstCard.isBetterThan(card):
				worstCard = card
		return worstCard

	# Returns the lowest valued cards in a list.
	def worstCardsInList(self, cardList):
		worstCards = []
		worstCard = cardList[0]
		for card in cardList:
			if worstCard.getRank() == card.getRank():
				worstCards.append(card)
			elif worstCard.isBetterThan(card):
				worstCards = [card]
				worstCard = card
		return worstCards

# An Agent that uses basic, intuitive heuristics, falling back on a 
# greedy approach when no heuristics are applicable.
class HeuristicAgent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.type = "HeuristicAgent"
		self.pileRep = util.Stack()		# Internal representation of the pile.
		self.discardPileRep = []	# Internal representation of the discard pile.
		self.opponentHandRep = []	# Internal representation of the opponent's hand.
		self.deckSize = 52 - 18

	def getID(self):
		return self.agentID

	def getType(self):
		return self.type

	# Apply heuristics if possible, otherwise be greedy.
	def chooseHandCard(self, hand, upCards, playableCards):
		if playableCards == []:
			return []

		# If 7s and 6s are in hand and playable, play 7s first.
		elif self.sevensRule(hand, playableCards):
			return self.getAllOfRank(7, playableCards)

		# If pile is getting large and opponent has a 3, try to clear the pile.
		#elif self.containsRank(self.opponentHandRep, 5) and self.pileRep.size() >= 5 and (self.containsRank(playableCards, 3) or self.containsRank(playableCards, 10)):
			#if self.containsRank(playableCards, 3):
				#return self.getOneOfRank(3, playableCards)
			#if self.containsRank(playableCards, 10):
				#return self.getOneOfRank(10, playableCards)

		# If we can only play face cards, play only one of the lowest playable rank.
		# minRank = self.lowestRank(playableCards)
		# if minRank > 10 and self.deckSize > 0:

		# 	return self.getOneOfRank(minRank, playableCards)

		# If we can only play wilds, play one of the least valuable kind.
		# elif self.onlyWilds(playableCards) and self.deckSize > 0:
		# 	if self.containsRank(playableCards, 2):
		# 		return self.getOneOfRank(2, playableCards)
		# 	elif self.containsRank(playableCards, 10):
		# 		return self.getOneOfRank(10, playableCards)
		# 	elif self.containsRank(playableCards, 3):
		# 		return self.getOneOfRank(3, playableCards)

		elif self.onlyWilds(playableCards):
			if self.containsRank(playableCards, 2):
				return self.getOneOfRank(2, playableCards)
			elif self.containsRank(playableCards, 10):
				return self.getOneOfRank(10, playableCards)
			elif self.containsRank(playableCards, 3):
				return self.getOneOfRank(3, playableCards)

		# Greedy case: play all of lowest playable rank.
		else:
			return self.worstCardsInList(playableCards)

	# Apply heuristics if possible, otherwise be greedy.
	def chooseUpCard(self, upCards, playableCards):
		if playableCards == []:
			return []
		elif self.sevensRule(upCards, playableCards):
			return self.getAllOfRank(7, playableCards)

		# If we can only play face cards, play only one of the lowest playable rank.
		minRank = self.lowestRank(playableCards)
		if minRank > 10:
			return self.getOneOfRank(minRank, playableCards)

		# If we can only play wilds, play one of the least valuable kind.
		elif self.onlyWilds(playableCards):
			if self.containsRank(playableCards, 2):
				return self.getOneOfRank(2, playableCards)
			elif self.containsRank(playableCards, 10):
				return self.getOneOfRank(10, playableCards)
			elif self.containsRank(playableCards, 3):
				return self.getOneOfRank(3, playableCards)

		# Greedy case: play all of lowest playable rank.
		else:
			return self.worstCardsInList(playableCards)

	def chooseDownCard(self):
		return

	# Swap best card in hand with worst card in up cards until
	# there are no more productive swaps.
	def chooseSwap(self, hand, upCards, playableCards):
		bestHandCard = self.bestCardInList(hand)
		worstUpCard = self.worstCardInList(upCards)
		# If there are no more productive swaps, play lowest card(s).
		if not bestHandCard.isBetterThan(worstUpCard):
			worstHandCards = self.worstCardsInList(playableCards)
			return (None, worstHandCards)
		
		# Return a valid swap.
		else:
			return (worstUpCard, bestHandCard)

	# Update knowledge based on percept.
	# cardList only given on "PLAY" move.
	# agentID only used on "PICKUP" and "PLAY".
	# handCard only used on "SWAP", where cardList is an up card.
	# On "DRAW", cardList = # of cards drawn.
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		if perceptType == "PICKUP":
			while not self.pileRep.isEmpty():
				card = self.pileRep.pop()
				if card.getRank() == 3:
					self.discardPileRep.append(card)
				else:
					if not agentID == self.getID():
						self.opponentHandRep.append(card)
		elif perceptType == "DISCARD":
			while not self.pileRep.isEmpty():
				card = self.pileRep.pop()
				self.discardPileRep.append(card)
		elif perceptType == "PLAY":
			for card in cardList:
				if not agentID == self.getID() and card in self.opponentHandRep:
					self.opponentHandRep.remove(card)
				self.pileRep.push(card)
		elif perceptType == "SWAP":
			upCard = cardList
			handCard = handCard
			if not agentID == self.getID():
				if handCard in self.opponentHandRep:
					self.opponentHandRep.remove(handCard)
				self.opponentHandRep.append(upCard)
		elif perceptType == "DRAW":
			self.deckSize -= cardList
		else:
			print "INVALID PERCEPT TYPE"
		return

	#######################################################
	#######################################################
	# HELPER METHODS
	#######################################################
	#######################################################

	# Return a list of all cards in playableCards of a certain rank.
	def getAllOfRank(self, rank, playableCards):
		output = []
		for card in playableCards:
			if card.getRank() == rank:
				output.append(card)
		return output

	# Returns a list containing a single card of a single rank from playableCards.
	def getOneOfRank(self, rank, playableCards):
		for card in playableCards:
			if card.getRank() == rank:
				return [card]

	# Return one of the best cards in a list.
	def bestCardInList(self, cardList):
		bestCard = cardList[0]
		for card in cardList:
			if card.isBetterThan(bestCard):
				bestCard = card
		return bestCard

	# Return one of the worst cards in a list.
	def worstCardInList(self, cardList):
		worstCard = cardList[0]
		for card in cardList:
			if worstCard.isBetterThan(card):
				worstCard = card
		return worstCard

	# Returns the lowest valued cards in a list.
	def worstCardsInList(self, cardList):
		worstCards = []
		worstCard = cardList[0]
		for card in cardList:
			if worstCard.getRank() == card.getRank():
				worstCards.append(card)
			elif worstCard.isBetterThan(card):
				worstCards = [card]
				worstCard = card
		return worstCards

	# Returns True iff sevens rule is applicable.
	def sevensRule(self, hand, playableCards):
		if self.containsRank(playableCards, 7) and self.containsRank(hand, 6):
			return True
		else:
			return False

	# Returns True iff cardList contains only wilds.
	def onlyWilds(self, cardList):
		for card in cardList:
			if not card.isWild(): 
				return False
		return True

	# Returns True iff cardList contains at least one
	# card of a certain rank.
	def containsRank(self, cardList, rank):
		for card in cardList:
			if card.getRank() == rank:
				return True
		return False

	# Return the lowest rank in cardList.
	def lowestRank(self, cardList):
		minRank = cardList[0]
		for card in cardList:
			if card.getRank() < minRank:
				minRank = card.getRank()
		return minRank

	def oppHandRepToString(self):
		output = ""
		for card in self.opponentHandRep:
			output += card.toString() + " "
		return "[" + output + "]"

	def discardRepToString(self):
		output = ""
		for card in self.discardPileRep:
			output += card.toString() + " "
		return "[" + output + "]"

	def pileRepToString(self):
		return self.pileRep.toString()

	def getDeckSize(self):
		return str(self.deckSize)

# BROKEN, please fix.
class HumanAgent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.pileRep = util.Stack()	# Internal representation of the pile.
		self.discardPileRep = {}	# Internal representation of the discard pile.
		self.opponentHandRep = {}	# Internal representation of the opponent's hand.

	def getID(self):
		return self.agentID

	def chooseHandCard(self, hand, upCards, playableCards):
		rankToPlay = input("Enter the rank of the card/cards you want to play: ")
		quantityToPlay = input("Enter the number of cards you want to play:" )

		input = (rankToPlay, quantityToPlay)
		action = getActionFromInput(playableCards, quantityToPlay)

		return action

	# Choose the lowest playable cards.
	def chooseUpCard(self, upCards, playableCards):
		rankToPlay = input("Enter the rank of the card/cards you want to play: ")
		quantityToPlay = input("Enter the number of cards you want to play:" )

		input = (rankToPlay, quantityToPlay)
		action = getActionFromInput(playableCards, quantityToPlay)

		return action

	# Trivial; return.
	def chooseDownCard(self):
		return

	# First input decide's whether to swap or to play.
	# if play, calls the chooseHandCard() function
	# else takes keyboard input to choose the cards to be swapped
	# Tuple of chosen cards is returned if it is legal. checked at input stage.
	# If we want to play a card, return (None, cardList).
	def chooseSwap(self, hand, upCards, playableCards):

		wantToSwap = 0
		while(wantToSwap != 1 or wantToSwap != 9):
			wantToSwap = input("Enter 1 to make a swap or 9 to take the first turn.")


			if wantToSwap == 1:
				handCardRank = input("Choose the rank of your hand-card: ")
				handCardSuit = input("Choose the suit of your hand-card: ")
				upCardRank = input("Choose the rank of your up-card: ")
				upCardRank = input("Choose the rank of your up-card: ")
				chosenHandCard = util.Card(handCardRank, handCardSuit)
				chosenUpCard = util.Card(upCardRank, upCardSuit)
				return (chosenUpCard, chosenHandCard)

			else:
				return (None, worstHandCards)

	# Update knowledge based on percept.
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		return

	# Accepts a tuple as input (rank, quantity) and converts it to an action list
	# returns an empty list if the cards are not available
	def getActionFromInput(self, playableCards, input):
		action = []
		counter = input[1] #keeps track of the number of cards to be played
		for card in playAbleCards:
			if (card.getRank() == input[0]):
				action.append(card)
				counter -= 1
			if counter == 0: break

		if(counter != 0): action = [] #returns an empty(invalid) list if the cards were not available
		return action


class LearningAgent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.type = "LearningAgent"
		self.pileRep = util.Stack()		# Internal representation of the pile.
		self.discardPileRep = []	# Internal representation of the discard pile.
		self.opponentHandRep = []	# Internal representation of the opponent's hand.
		self.deckSize = 52 - 18
		self.weights = dict()
