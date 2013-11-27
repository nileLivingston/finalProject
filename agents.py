import util
import random

# An agent that randomly chooses actions.
class RandomAgent:

	def __init__(self, agentID):
		self.agentID = agentID

	def getID(self):
		return self.agentID

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

	# Trivial; return.
	def chooseDownCard(self):
		return

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

	# Randomly chooses a legal swap or to begin turn-taking.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return (None, cardList).
	def chooseSwap(self, hand, upCards, playableCards):
		# Randomly choose between swapping and putting down.
		handPlay = [random.choice(hand)]
		return (None, handPlay)
		
		# Return a valid swap.
		upSwap = random.choice(upCards)
		handSwap = random.choice(hand)
		return (upSwap, handSwap)

	# Swap best card in hand with worst card in up cards until
	# there are no more productive swaps.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return (None, cardList).
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		return

class GreedyAgent:

	def __init__(self, agentID):
		self.agentID = agentID

	def getID(self):
		return self.agentID

	# Choose the lowest playable cards.
	def chooseHandCard(self, hand, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			return self.worstCardsInList(playableCards)

	# Choose the lowest playable cards.
	def chooseUpCard(self, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			return self.worstCardsInList(playableCards)

	# Trivial; return.
	def chooseDownCard(self):
		return

	# Swap best card in hand with worst card in up cards until
	# there are no more productive swaps.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return (None, cardList).
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

	# Swap best card in hand with worst card in up cards until
	# there are no more productive swaps.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return (None, cardList).
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		return

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

class HeuristicAgent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.pileRep = util.Stack()		# Internal representation of the pile.
		self.discardPileRep = []	# Internal representation of the discard pile.
		self.opponentHandRep = []	# Internal representation of the opponent's hand.

	def getID(self):
		return self.agentID

	# Choose the lowest playable cards.
	def chooseHandCard(self, hand, upCards, playableCards):
		if playableCards == []:
			return []
		elif self.sevensRule(hand, playableCards):
			return self.getAllOfRank(7, playableCards)
		else:
			return self.worstCardsInList(playableCards)

	# Choose the lowest playable cards.
	def chooseUpCard(self, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			return self.worstCardsInList(playableCards)

	# Trivial; return.
	def chooseDownCard(self):
		return

	# Swap best card in hand with worst card in up cards until
	# there are no more productive swaps.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return (None, cardList).
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

	# Return a list of all cards in playableCards of a certain rank.
	def getAllOfRank(self, rank, playableCards):
		output = []
		for card in playableCards:
			if card.getRank() == rank:
				output.append(card)
		return output

	# Update knowledge based on percept.
	# cardList only given on "PLAY" move.
	# agentID only used on "PICKUP" and "PLAY".
	# handCard only used on "SWAP", where cardList is an up card.
	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
		if perceptType == "PICKUP":
			if not agentID == self.getID():
				while not self.pileRep.isEmpty():
					card = self.pileRep.pop()
					self.opponentHandRep.append(card)
		elif perceptType == "DISCARD":
			while not self.pileRep.isEmpty():
				card = self.pileRep.pop()
				self.discardPileRep.append(card)
		elif perceptType == "PLAY":
			if not agentID == self.getID():
				for card in cardList:
					self.pileRep.push(card)
		elif perceptType == "SWAP":
			upCard = cardList
			handCard = handCard
			if handCard in self.opponentHandRep:
				self.opponentHandRep.remove(handCard)
			self.opponentHandRep.append(upCard)
		else:
			print "INVALID PERCEPT TYPE"
		return

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

	# Returns True iff cardList contains at least one
	# card of a certain rank.
	def containsRank(self, cardList, rank):
		for card in cardList:
			if card.getRank() == rank:
				return True
		return False

	def oppHandRepToString(self):
		output = "["
		for card in self.opponentHandRep:
			output += card.toString() + " "
		output += "]"