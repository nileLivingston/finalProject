import random

# Represents an instance of a Scheisskopf game. Handles all control related to
# turn-taking and GameBoard manipulation.
class Game:

	# Construct players and GameBoard.
	def __init__(self, playerOneHuman):
		self.inPregame = True
		self.playerOne = RandomAgent(1)
		self.playerTwo = RandomAgent(2)
		self.players = [self.playerOne, self.playerTwo]

		self.gameBoard = GameBoard(self.players)
		self.activePlayer = self.playerOne

	def getGameBoard(self):
		return self.gameBoard

	# Moves the game forward a single turn and change activePlayer.
	def takeTurn(self):
		# If we're in the pregame, take turns swapping.
		if self.inPregame:
			swap = self.activePlayer.chooseSwap()

			# Check to see if swap is the first normal turn.
			if len(swap) == 1:


			# Check legality of swap and apply if necessary.
			else:
				upCard = swap[0]
				handCard = swap[1]
				if self.gameBoard.isLegalSwap(activePlayer):
					gameBoard.applySwap()
					# Send percepts to all players.
					for player in self.players:

					return

		# If we're doing normal turn taking, make activePlayer take a turn.	
		else:
			pileCard = gameBoard.peekPile()
			
			# Down cards are available for player. No need to actually choose; random anyway.
			if gameBoard.viewUpCards(activePlayer) == [] and gameBoard.viewHand(activePlayer) == {}:
				downCardPlay(activePlayer, pileCard)
				return

			# Up cards are available for player.
			elif gameBoard.viewHand == {}:
				upCardPlay(activePlayer, pileCard)
				return

			# Player still has a hand to play.
			else:
				handCardsPlay(activePlayer, pileCard)
				return

		# Hand over turn-taking control.
		if self.activePlayer == self.playerOne:
			self.activePlayer = self.playerTwo
		else:
			self.activePlayer = self.playerOne

	# Handles the playing of a down card.
	def downCardPlay(self, activePlayer, pileCard):
		# Select a down card and put it on the pile.
		activePlayer.chooseDownCard()	
		index = random.choice(range(0, len(self.gameBoard.downCards(activePlayer))))
		downCard = self.gameBoard.downCards.pop(index)
		self.gameBoard.downCardToPile(downCard)
				
		# If the card is not playable on the pile, pick it all up.
		if not downCard.isPlayableOn(pileCard):
			self.gameBoard.pileToHand(activePlayer)

	# Handles the playing of an up card.
	def upCardPlay(self, activePlayer, pileCard):
		playableCards = self.gameBoard.getPlayableUpCards(self.activePlayer)
		action = activePlayer.chooseUpCard(playableCards)
		# Make sure a null action is true. If so, pick up pile.
		if action == []:
			if playableCards == []:
				pileToHand(activePlayer)
			else:
				return

		# Check to see if action is valid. If so, play cards.
		for card in action:
			# Invalid move: reject.
			if not card.isPlayableOn(pileCard):
				return
			# If all valid, push to pile.
		self.gameBoard.handToPile(player, action)

	# Handles the playing of hand cards.
	def handCardsPlay(self, activePlayer, pileCard):
		playableCards = self.gameBoard.getPlayableHandCards(self.activePlayer)
		action = activePlayer.chooseHandCard(playableCards)
		# Make sure a null action is true. If so, pick up the pile.
		if action == []:
			if playableCards == []:
				pileToHand(activePlayer)
			else:
				return

		# Check to see if action is valid. If so, play cards.
		for card in action:
			# Invalid move: reject.
			if not card.isPlayableOn(pileCard):
				return
		# If all valid, push to pile.
		self.gameBoard.handToPile(player, action)
		return


# Represents a configuration of the cards on the table and in players' hands.
class GameBoard:

	def __init__(self, players):
		self.pile = Stack()
		self.deck = Stack()
		self.discard = Stack()
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
				newCard = Card(rank, suit)
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

			self.hands[ID] = set()
			# Draw a 3-card hand for the player.
			for i in range(1, 4):
				self.hands[ID].add(self.deck.pop())

	# TOSTRING() METHODS ARE TEMPORARY!
	# After we get the GUI up and running, we can
	# cut these.
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

	# Returns True iff game is over.
	def isTerminal(self):
		for player in self.players:
			if self.downCards[player] == {}:
				return True

	# Returns the card on top of the pile.
	def peekPile(self):
		return self.pile.peek()

	# Returns the card on top of the discard pile.
	def peekDiscard(self):
		return self.discard.peek()

	# Returns a copy of the hand for player.
	def viewHand(self, player):
		return set(hands[player])

	# Returns a copy of the player's up cards.
	def viewUpCards(self, player):
		return list(self.upCards[player])

	# Returns a copy of the player's down cards.
	def downCards(self, player):
		return list(self.downCards[player])

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
		for card in self.upCards[player.get()]:
			if card.isPlayableOn(pileCard):
				playableCards.append(card)
		return playableCards

	# Changes the GameBoard as a result of an action and
	# sends out percepts.
	def enactAction(self, action):
		return

	# Places cards from an players's hand into the pile.
	def handToPile(self, player, cardList):
		hand = self.hands[player.getID()]
		for card in cardList:
			hand.remove(card)
			self.pile.push(card)

	# Places cards from the pile into the agent's hand.
	def pileToHand(self, player):
		hand = self.hands[player.getID()]
		while not self.pile.isEmpty():
			card = self.pile.pop()
			hand.add(card)

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
			discard.push(card)
		self.discard.push(topCard)

	# Applies a swap. 
	def applySwap((upSwap, handSwap), player):
		ID = player.getID()
		upCards = self.upCards[ID]
		hand = self.hands[ID]
		upCards.remove(upSwap)
		hand.add(upSwap)
		hand.remove(handSwap)
		upCards.append()

# Represents a single card object with rank, suit, and wildness.
class Card:

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
		if self.rank == 2 or self.rank == 3 or self.rank == 10:
			self.wild = True
		else:
			self.wild = False

	def getRank(self):
		return self.rank

	def getSuit(self):
		return self.suit

	def isWild(self):
		return self.wild

	# TOSTRING METHOD IS TEMPORARY!
	# Once we get the GUI up and running, we
	# can cut this. 
	def toString(self):
		translatedRank = ""
		if self.rank == 11:
			translatedRank = "J"
		elif self.rank == 12:
			translatedRank = "Q"
		elif self.rank == 13:
			translatedRank = "K"
		elif self.rank == 14:
			translatedRank = "A"
		else:
			translatedRank = str(self.rank)

		return translatedRank + str(self.suit)

	# Returns True iff this card is playable (by Scheisskopf rules) on otherCard.
	def isPlayableOn(self, otherCard):
		if otherCard.rank == 3 or otherCard.rank == 10:
			return False
		elif self.wild:
			return True
		elif otherCard.rank == 7 and self.rank <= 7:
			return True
		elif self.rank >= otherCard.rank:
			return True
		else:
			return False


# A general purpose, last in first out (LIFO) data structure.
# In our implementation, used for representing stacks of Cards.
class Stack:

	# Elements of the stack are stored in a list, where the last element of the list
	# is topmost in the stack.
	def __init__(self):
		self.list = []

	# Removes the topmost element from the stack and returns it.
	def pop(self):
		return self.list.pop()

	# Adds item to the stack, making it the new topmost element.
	def push(self, item):
		self.list.append(item)

	# Push an entire list onto the stack. Note that the last element of the list
	# becomes the new topmost element of the stack.
	def pushList(self, list):
		for item in list:
			self.list.append(item)

	# Returns the number of elements in the stack.
	def size(self):
		return len(self.list)

	# Returns true iff stack is empty.
	def isEmpty(self):
		return self.size() == 0

	# Returns the item topmost in the stack.
	def peek(self):
		index = self.size() - 1
		return self.list[index]

	# Returns a string representation of the stack.
	def toString(self):
		output = "["
		for item in self.list:
			output += item.toString() + " "
		output += "]"
		return output


# An agent that randomly chooses actions.
class RandomAgent:

	def __init__(self, agentID):
		self.agentID = agentID
		self.pileRep = Stack()	# Internal representation of the pile.
		self.discardPileRep = {}	# Internal representation of the discard pile.
		self.opponentHandRep = {}	# Internal representation of the opponent's hand.

		# Percept types:
		self.pickedUpPile = 1
		self.opponentPickedUpPile = 2
		self.playedCard = 1
		self.opponentPlayedCard = 2
		self.pickedUpPile = 1
		self.opponentPickedUpPile = 2
		self.unsuccessfulPlay = 5
		self.opponentUnsuccessfulPlay = 6

	def getID(self):
		return self.agentID

	# Randomly chooses a legal action.
	def chooseHandCard(self, hand, upCards, playableCards):
		return random.choice(playableCards)

	# Choose legal up card(s) to play.
	def chooseUpCard(self, upCards, playableCards):
		return random.choice(playableCards)

	# Trivial; return.
	def chooseDownCard(self):
		return

	# Randomly chooses a legal swap or to begin turn-taking.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return...?
	def chooseSwap(self, hand, topCards):
		hand = gameBoard.viewhand(self.agentID)
		upCards = gameBoard.viewUpCards()
		upSwap = random.choose(upCards)
		handSwap = random.choose(hand)
		return (upSwap, handSwap)

	# Update knowledge based on percept.
	def updateKnowledge(self, perceptType, cardList=None):
		return


# Main method used for testing.
if __name__ == '__main__':

	game = Game(True)
	gameBoard = game.getGameBoard()
	print gameBoard.deckToString()
	print gameBoard.handsToString()
	print gameBoard.upCardsToString()
	print gameBoard.downCardsToString()
