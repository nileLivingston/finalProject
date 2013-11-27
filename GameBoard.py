import util
import random

# Represents a configuration of the cards on the table and in players' hands.
class GameBoard:

	#######################################################
	#######################################################
	# CONSTRUCTOR:
	# Initializes and shuffles the deck, deals cards to 
	# players. Sets up all of the appropriate data
	# structures.
	#######################################################
	#######################################################

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
	# TOSTRING() METHODS:
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

	# Returns True iff player can legally make swap
	def isLegalSwap(self, upCard, handCard, player):
		upCards = self.upCards[player.getID()]
		hand = self.hands[player.getID()]
		if upCard in upCards and handCard in hand:
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

	# Places cards from an players's hand into the pile.
	def handToPile(self, player, cardList):
		hand = self.hands[player.getID()]
		for card in cardList:
			hand.remove(card)
			self.pile.push(card)

		self.draw(player)

	# Places cards from the pile into the agent's hand.
	def pileToHand(self, player):
		hand = self.hands[player.getID()]
		while not self.pile.isEmpty():
			card = self.pile.pop()
			hand.append(card)

	# Places cards from the player's up cards into the pile.
	def upCardsToPile(self, player, cardList):
		upCards = self.upCards[player.getID()]
		for card in cardList:
			upCards.remove(card)
			self.pile.push(card)

	# Places a single down card on the pile.
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

	# Applies a swap, assuming it's legal.
	def applySwap(self, swap, player):
		upSwap = swap[0]
		handSwap = swap[1]
		ID = player.getID()
		upCards = self.upCards[ID]
		hand = self.hands[ID]
		upCards.remove(upSwap)
		hand.append(upSwap)
		hand.remove(handSwap)
		upCards.append(handSwap)

	# Make player draw the necessary number of cards.
	def draw(self, player):
		hand = self.hands[player.getID()]
		# Player must draw enough cards to have
		# at least 3 (if there are enough).
		cardsToDraw = min(3 - len(hand), self.deck.size())
		if cardsToDraw > 0:
			for i in range(0, cardsToDraw):
				card = self.deck.pop()
				hand.append(card)

	# Used to clear a 3 from the top of the pile.
	def clearTopCard(self):
		topCard = self.pile.pop()
		self.discard.push(topCard)