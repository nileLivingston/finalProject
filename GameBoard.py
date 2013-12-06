import util
import random

# Represents a configuration of the cards on the table and in players' hands.
class GameBoard:

	# Initializes and shuffles the deck, deals cards to 
	# players. Sets up all of the appropriate data
	# structures.
	def __init__(self, players):
		self.pile = util.Stack()
		self.deck = util.Stack()
		self.discard = util.Stack()
		self.players = players

		# Dict with mappings player:set
		self.hands = dict()		
		# Dicts with mappings agentID:list
		self.upCards = dict()		
		self.downCards = dict()

		# Initialize and shuffle the deck
		tempDeck = []
		for suit in ["C", "S", "D", "H"]:
			for rank in range(2, 15):
				newCard = util.Card(rank, suit)
				tempDeck.append(newCard)
		random.shuffle(tempDeck)
		self.deck.pushList(tempDeck)	

		for player in self.players:
			ID = player.getID()
			# Draw 3 down cards for the player.
			self.downCards[ID] = []
			for i in range(1, 4):
				self.downCards[ID].append(self.deck.pop())

			self.upCards[ID] = []
			# Draw 3 up cards for the player.
			for i in range(1, 4):
				self.upCards[ID].append(self.deck.pop())

			self.hands[ID] = []
			# Draw a 3-card hand for the player.
			for i in range(1, 4):
				self.hands[ID].append(self.deck.pop())

	#######################################################
	#######################################################
	# toString Methods:
	# These are mainly useful for debugging in the terminal.
	#######################################################
	#######################################################

	def deckToString(self):
		return "Deck: " + self.deck.toString()

	def handsToString(self):
		output = "Hands: "
		for player in self.players:
			ID = player.getID()
			hand = self.hands[ID]
			output += "("
			for card in hand:
				output += card.toString() + " "
			output += ") "
		return output

	def upCardsToString(self):
		output = "Up cards: "
		for player in self.players:
			ID = player.getID()
			upCards = self.upCards[ID]
			output += "("
			for card in upCards:
				output += card.toString() + " "
			output += ") "
		return output

	def downCardsToString(self):
		output = "Down cards: "
		for player in self.players:
			ID = player.getID()
			downCards = self.downCards[ID]
			output += "("
			for card in downCards:
				output += card.toString() + " "
			output += ") "
		return output

	def pileToString(self):
		return "Pile: " + self.pile.toString()

	def discardToString(self):
		return "Discard: " + self.discard.toString()

	#######################################################
	#######################################################
	# BOOLEAN ACCESSOR METHODS:
	# Gets True or False values about the GameBoard or 
	# things in it.
	#######################################################
	#######################################################

	#CHANGES  -  areEqual and inList

	def areEqual(self, card1, card2):
		card1rank = card1.getRank()
		card2rank = card2.getRank()

		if card1rank == "A": card1rank = 14
		if card1rank == "J": card1rank = 11
		if card1rank == "Q": card1rank = 12
		if card1rank == "K": card1rank = 13

		if card2rank == "A": card2rank = 14
		if card2rank == "J": card2rank = 11
		if card2rank == "Q": card2rank = 12
		if card2rank == "K": card2rank = 13

		return (card1rank == card2rank and card1.getSuit() == card2.getSuit())

	def inList(self, card, cardList):
		for listCard in cardList:
			if self.areEqual(card, listCard): return True
		return False

	# Returns True iff game is over.
	def isTerminal(self):
		for player in self.players:
			if self.downCards[player.getID()] == [] and self.hands[player.getID()] == []:
				return True

	# Returns True iff down cards are playable for player with agentID.
	def downCardsPlayable(self, agentID):
		return self.upCards[agentID] == [] and self.hands[agentID] == []

	# Returns True iff up cards are playable for player with agentID.
	def upCardsPlayable(self, agentID):
		return self.hands[agentID] == [] and not self.upCards[agentID] == []

	# Returns true iff the top four cards of the pile are the same.
	def topFourSame(self):
		if self.pile.size() < 4:
			return False
		output = True
		temp = util.Stack()
		card = self.pile.pop()
		temp.push(card)
		oldRank = card.getRank()
		for i in range(1, 4):
			card = self.pile.pop()
			temp.push(card)
			rank = card.getRank()
			if not rank == oldRank:
				output = False
				break
		while not temp.isEmpty():
			card = temp.pop()
			self.pile.push(card)
		return output

	# # Returns True iff player can legally make swap
	# def isLegalSwap(self, upCard, handCard, player):
	# 	upCards = self.upCards[player.getID()]
	# 	hand = self.hands[player.getID()]
	# 	if upCard in upCards and handCard in hand:
	# 		return True
	# 	else:
	# 		return False

	# Returns True iff player can legally make swap
	# CHANGES MADE - uses inList()
	def isLegalSwap(self, upCard, handCard, player):

		upCards = self.upCards[player.getID()]
		hand = self.hands[player.getID()]

		if self.inList(upCard, upCards) and self.inList(handCard, hand):
			return True
		else:
			return False

	# Returns True iff player can legally play upCardsToPlay.
	def isLegalUpCardPlay(self, upCardsToPlay, player):
		pileCard = self.pile.peek()
		upCards = self.upCards[player.getID()]
		# If action is empty, make sure playableCards is empty too.
		if upCardsToPlay == []:
			playableCards = self.getPlayableUpCards(player)
			if playableCards == []:
				return True
			else:
				return False

		# If action nonempty, check that all cards are in upCards, same rank, and playable on pile.		
		if not self.allSameRank(upCardsToPlay):
			return False	
		for upCard in upCardsToPlay:
			if not upCard in upCards or not upCard.isPlayableOn(pileCard):
				return False
		return True

	# Returns True iff player can legally play handCardsToPlay.
	def isLegalHandCardPlay(self, handCardsToPlay, player):
		pileCard = self.pile.peek()
		hand = self.hands[player.getID()]
		# If action is empty, make sure playableCards is empty too.
		if handCardsToPlay == []:
			playableCards = self.getPlayableHandCards(player)
			if playableCards == []:
				return True
			else:
				return False

		# If action nonempty, check that all cards are in hand, same rank, and playable on pile.	
		if not self.allSameRank(handCardsToPlay):
			return False		
		for handCard in handCardsToPlay:
			if not handCard in hand or not handCard.isPlayableOn(pileCard):
				return False
		return True

	# Returns True iff all cards in cardList have same rank.
	def allSameRank(self, cardList):
		oldRank = cardList[0].getRank()
		for card in cardList:
			rank = card.getRank()
			if not rank == oldRank:
				return False
		return True

	#######################################################
	#######################################################
	# NON-BOOLEAN ACCESSOR METHODS:
	# Used to access different attributes of the GameBoard
	#######################################################
	#######################################################

	# Returns the card on top of the pile.
	def peekPile(self):
		return self.pile.peek()

	# Returns the card on top of the discard pile.
	def peekDiscard(self):
		return self.discard.peek()

	# Returns a copy of the hand for player.
	def viewHand(self, player):
		return list(self.hands[player.getID()])

	# Returns a copy of the player's up cards.
	def viewUpCards(self, player):
		return list(self.upCards[player.getID()])

	# Returns a copy of the player's down cards.
	def viewDownCards(self, player):
		return list(self.downCards[player.getID()])

	# Returns a list of legal hand cards for an agent. [] implies no legal hand cards.
	def getPlayableHandCards(self, player):
		playableCards = []
		pileCard = self.pile.peek()
		for card in self.hands[player.getID()]:
			if card.isPlayableOn(pileCard):
				playableCards.append(card)
		return playableCards

	# Returns a list of legal up cards for an agent. [] implies no legal up cards.
	def getPlayableUpCards(self, player):
		playableCards = []
		pileCard = self.pile.peek()
		for card in self.upCards[player.getID()]:
			if card.isPlayableOn(pileCard):
				playableCards.append(card)
		return playableCards

	#######################################################
	#######################################################
	# MUTATOR METHODS:
	# These methods make changes to the GameBoard.
	#######################################################
	#######################################################

	# Places cards from player's hand into the pile.
	def handToPile(self, player, cardList):
		hand = self.hands[player.getID()]
		for card in cardList:
			hand.remove(card)
			self.pile.push(card)

		numDrawn = self.draw(player)
		return numDrawn

	# Places cards from the pile into player's hand.
	def pileToHand(self, player):
		hand = self.hands[player.getID()]
		while not self.pile.isEmpty():
			card = self.pile.pop()
			hand.append(card)

	# Places cards from player's up cards into the pile.
	def upCardsToPile(self, player, cardList):
		upCards = self.upCards[player.getID()]
		for card in cardList:
			upCards.remove(card)
			self.pile.push(card)

	# Places one of player's down cards on the pile.
	def downCardToPile(self, player, card):
		downCards = self.downCards[player.getID()]
		downCards.remove(card)
		self.pile.push(card)

	# Sends the pile to the discard pile.
	def clearPile(self):
		topCard = self.pile.pop()
		while not self.pile.isEmpty():
			card = self.pile.pop()
			self.discard.push(card)
		self.discard.push(topCard)

	# Used to clear 3s from the top of the pile.
	def clearThrees(self):
		done = False
		while not done:
			topCard = self.pile.peek()
			if not topCard == None and topCard.getRank() == 3:
				self.pile.pop()
				self.discard.push(topCard)
			else:
				done = True

	# Applies a swap, assuming it's legal.
	def applySwap(self, swap, player):
		upSwap = swap[0]
		handSwap = swap[1]
		ID = player.getID()
		upCards = self.upCards[ID]
		hand = self.hands[ID]

		for card in upCards:
			if self.areEqual(upSwap, card):
				upCards.remove(card)
				hand.append(upSwap)
				break
		for card in hand:
			if self.areEqual(card, handSwap):
				hand.remove(card)
				upCards.append(card)
				break

		"""
		works for nonHuman agents because comapares object addresses

		upCards.remove(upSwap)
		hand.append(upSwap)
		hand.remove(handSwap)
		upCards.append(handSwap)

		"""

	# Make player draw the necessary number of cards.
	# Returns number of cards drawn in order to send percepts.
	def draw(self, player):
		hand = self.hands[player.getID()]
		# Player must draw enough cards to have
		# at least 3 (if there are enough).
		cardsToDraw = min(3 - len(hand), self.deck.size())
		if cardsToDraw > 0:
			for i in range(0, cardsToDraw):
				card = self.deck.pop()
				hand.append(card)
			return cardsToDraw
		else:
			return 0 

	