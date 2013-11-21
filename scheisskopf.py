import random

# Represents an instance of a Scheisskopf game. Handles all control related to
# turn-taking and GameBoard manipulation.
class Game:

	def __init__(self, playerOneHuman):
		self.inPregame = True
		self.playerOne = RandomAgent()
		self.playerTwo = RandomAgent()
		self.players = [self.playerOne, self.playerTwo]

		self.gameBoard = GameBoard(self.players)
		self.activePlayer = self.playerOne

	# Moves the game forward a single turn and change activePlayer.
	def takeTurn(self):
		# If we're in the pregame, take turns swapping.
		if self.inPregame:
			swap = self.activePlayer.chooseSwap()
			

		# If we're doing normal turn taking, make activePlayer take a turn.	
		else:
			pileCard = gameBoard.peekPile()
			
			# Down cards are available for player. No need to actually choose; random anyway.
			if gameBoard.viewUpCards(activePlayer) == [] and gameBoard.viewHand(activePlayer) == {}:
				# Select a down card and put it on the pile.
				activePlayer.chooseDownCard()	
				index = random.choice(range(0, len(gameBoard.downCards(activePlayer))))
				downCard = gameBoard.downCards.pop(index)
				gameBoard.downCardToPile(downCard)
				
				# If the card is not playable on the pile, pick it all up.
				if not downCard.isPlayableOn(pileCard):
					gameBoard.pileToHand(activePlayer)

			# Up cards are available for player.
			elif gameBoard.viewHand == {}:
				playableCards = gameBoard.getPlayableUpCards(self.activePlayer)
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
				gameBoard.handToPile(player, action)

			# Player still has a hand to play.
			else:
				playableCards = gameBoard.getPlayableHandCards(self.activePlayer)
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
				gameBoard.handToPile(player, action)


		# Hand over turn-taking control.
		if self.activePlayer == self.playerOne:
			self.activePlayer = self.playerTwo
		else:
			self.activePlayer = self.playerOne


# Represents a configuration of the cards on the table and in players' hands.
class GameBoard:

	def __init__(self, players):
		self.pile = Stack()
		self.deck = Stack()
		self.discard = Stack()
		self.players = players

		# Dict with mappings player:set
		self.hands = dict()		
		# Dicts with mappings player:list
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
			# Draw 3 down cards for the player.
			for i in range(1, 4):
				self.downCards[player].append(self.deck.pop())

			# Draw 3 up cards for the player.
			for i in range(1, 4):
				self.upCards[player].append(self.deck.pop())

			# Draw a 3-card hand for the player.
			for i in range(1, 4):
				self.hands[player].add(self.deck.pop())

	# For debugging.
	def deckToString(self):
		return self.deck.toString()

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
		for card in self.hands[player]:
			if card.isPlayableOn(pileCard):
				playableCards.append(card)
		return playableCards

	# Returns a list of legal up cards for an agent. [] implies no legal up cards.
	def getPlayableUpCards(self, player):
		playableCards = []
		pileCard = self.pile.peek()
		for card in self.upCards[player]:
			if card.isPlayableOn(pileCard):
				playableCards.append(card)
		return playableCards

	# Changes the GameBoard as a result of an action and
	# sends out percepts.
	def enactAction(self, action):
		return

	# Places cards from an players's hand into the pile.
	def handToPile(self, player, cardList):
		hand = self.hands[player]
		for card in cardList:
			hand.remove(card)
			self.pile.push(card)

	# Places cards from the pile into the agent's hand.
	def pileToHand(self, player):
		hand = self.hands[player]
		while not self.pile.isEmpty():
			card = self.pile.pop()
			hand.add(card)

	# Places cards from the player's up cards into the pile.
	def upCardsToPile(self, player, cardList):
		upCards = self.upCards[player]
		for card in cardList:
			upCards.remove(card)
			self.pile.push(card)

	def downCardToPile(self, player, card):
		downCards = self.downCards[player]
		downCards.remove(card)
		self.pile.push(card)

	# Sends the pile to the discard pile.
	def clearPile(self):
		topCard = self.pile.pop()
		while not self.pile.isEmpty():
			card = self.pile.pop()
			discard.push(card)
		self.discard.push(topCard)

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

	# Returns a String representation of the card.
	def toString(self):

		# This translation nonsense is only important if we're printing cards
		# in Terminal. Once we get the GUI up and running, we might cut this.
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

	def __init__(self):
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
	def chooseSwap(self, hand, topCards):
		hand = gameBoard.viewhand(self.agentID)
		topCards = gameBoard.viewTopCards()

	# Update knowledge based on percept.
	def updateKnowledge(self, perceptType, cardList=None):
		return


# Main method used for testing.
if __name__ == '__main__':

	game = Game(True)
	print board.deckToString()

