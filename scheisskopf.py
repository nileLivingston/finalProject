import random

# Represents an instance of a Scheisskopf game. Handles all control related to
# turn-taking and GameBoard manipulation.
class Game:

	# Construct players and GameBoard.
	def __init__(self, playerOneHuman):
		self.inPregame = True
		self.playerOne = GreedyAgent(1)
		self.playerTwo = RandomAgent(2)
		self.players = [self.playerOne, self.playerTwo]

		self.gameBoard = GameBoard(self.players)
		self.activePlayer = random.choice(self.players)
		self.pileCard = None
		self.ended = False
		self.winner = None

	# Prints the current state of the game.
	def snapshot(self):
		print self.gameBoard.deckToString()
		print self.gameBoard.handsToString()
		print self.gameBoard.upCardsToString()
		print self.gameBoard.downCardsToString()
		print self.gameBoard.pileToString()
		print self.gameBoard.discardToString()
		print "Player: " + str(self.activePlayer.getID())
		print "\n"

	# Returns the GameBoard.
	def getGameBoard(self):
		return self.gameBoard

	# Returns the ID of the active player.
	def getActivePlayer(self):
		return self.activePlayer.getID()

	# True iff game is over.
	def isEnded(self):
		return self.ended

	# Returns the winner of the game.
	def getWinner(self):
		return self.winner

	# Moves the game forward a single turn and change activePlayer.
	def takeTurn(self):
		# Check to see if the game is ended.
		if self.gameBoard.isTerminal():
			self.ended = True
			self.changeActivePlayer()
			self.winner = self.activePlayer.getID()	
			return

		# Look at the card on top of the pile.
		self.pileCard = gameBoard.peekPile()
		
		# If there's a ten on the pile, clear and skip activePlayer's turn.
		if not self.pileCard == None and (self.pileCard.getRank() == 10 or gameBoard.topFourSame()):
			gameBoard.clearPile()
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("DISCARD")
			self.changeActivePlayer()
			return

		# If there's a three on the pile, discard the three, force activePlayer to
		# pick up pile and skip their turn.
		if not self.pileCard == None and self.pileCard.getRank() == 3:
			gameBoard.clearTopCard()
			gameBoard.pileToHand(self.activePlayer)
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
			if gameBoard.downCardsPlayable(self.activePlayer.getID()):
				self.downCardPlay()

			# Up cards are available for player.
			elif gameBoard.upCardsPlayable(self.activePlayer.getID()):
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
		hand = gameBoard.viewHand(self.activePlayer)
		upCards = gameBoard.viewUpCards(self.activePlayer)
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
				gameBoard.applySwap(swap, self.activePlayer)
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
				return

		# Check to see if action is valid. If so, play cards.
		if self.gameBoard.isLegalHandCardPlay(action, self.activePlayer):
			self.gameBoard.handToPile(self.activePlayer, action)
			# Send percepts to all players.
			for player in self.players:
				player.updateKnowledge("PLAY", self.activePlayer.getID(), action)
			self.changeActivePlayer()
			return


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
		temp = Stack()
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

# Represents a single card object with rank, suit, and wildness.
class Card:

	# Initializes the rank, suit, and wildness of the Card.
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

	# Returns a String representation of the Card.
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
		# Pile is empty.
		if otherCard == None:
			return True
		# Wild cards are playable on anything.
		elif self.wild:
			return True
		# 7's case.
		elif otherCard.rank == 7:
			if self.rank <= 7:
				return True
			else:
				return False
		# Normal case.
		else:
			if self.rank >= otherCard.getRank():
				return True
			else:
				return False

	# Returns True iff card is more valuable than otherCard.
	# Value order:
	# 3 > 10 > 2 > A > K > ... > 4
	def isBetterThan(self, otherCard):
		if otherCard.getRank() == 3:
			return False
		elif otherCard.getRank() == 10:
			if self.rank == 3:
				return True
			else:
				return False
		elif otherCard.getRank() == 2:
			if self.rank == 3 or self.rank == 10:
				return True
			else:
				return False
		else:
			if self.wild:
				return True
			else:
				if self.rank > otherCard.getRank():
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
		if not self.list == []:
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

	# Returns True iff stack is empty.
	def isEmpty(self):
		return self.size() == 0

	# Returns the item topmost in the stack.
	def peek(self):
		if self.isEmpty():
			return None
		index = self.size() - 1
		return self.list[index]

	# Returns a String representation of the stack.
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
		self.pileRep = Stack()		# Internal representation of the pile.
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

# Main method used for testing.
if __name__ == '__main__':

	wins = [0, 0, 0]
	trials = 1000
	numTurns = []
	printTrials = False
	threshold = 50000
	for i in range(1, trials+1):
		turns = 0
		game = Game(False)
		gameBoard = game.getGameBoard()
	
		if printTrials:
			game.snapshot()
		while not game.isEnded():
			if turns > threshold:
				break
			game.takeTurn()
			turns += 1
			if printTrials:
				game.snapshot()
		winner = game.getWinner()
		if winner == None:
			print "Game " + str(i) + ": Draw"
			wins[0] += 1
		else:
			print "Game " + str(i) + ": Player " + str(winner)
			wins[winner] += 1
		numTurns.append(turns)

	#winrates = [wins[0]/float(trials),wins[1]/float(trials), wins[2]/float(trials)]
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




