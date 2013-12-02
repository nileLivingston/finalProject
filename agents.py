import util, random, state, sys
import featureExtractor as fe

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
	# If player elects to take first turn, should return (None, handCards).
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

	# Randomly chooses a legal action by picking a rank
	# in its playable cards and playing some number (at least one)
	# of that rank.
	def chooseHandCard(self, hand, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			rank = random.choice(playableCards).getRank()
			cardsToPlay = self.getSomeOfRank(rank, playableCards)
			return cardsToPlay

	# Randomly chooses a legal action by picking a rank
	# in its playable cards and playing some number (at least one)
	# of that rank.
	def chooseUpCard(self, upCards, playableCards):
		if playableCards == []:
			return []
		else:
			rank = random.choice(playableCards).getRank()
			cardsToPlay = self.getSomeOfRank(rank, playableCards)
			return cardsToPlay

	def chooseDownCard(self):
		return

	# Randomly chooses a legal swap or to begin turn-taking.
	# Legal swaps are represented as (upCard, handCard) tuples.
	# If we want to play a card, return (None, cardList).
	# Taking of the first turn follows the same procedure in 
	# chooseHandCard.
	def chooseSwap(self, hand, upCards, playableCards):
		# Randomly choose between swapping and putting down.
		if random.choice([0, 1]) == 1:
			# Return a valid first play.
			rank = random.choice(playableCards).getRank()
			cardsToPlay = self.getSomeOfRank(rank, playableCards)
			return (None, cardsToPlay)
		
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

	# # Return a list of all cards in playableCards of a certain rank.
	# def getAllOfRank(self, rank, playableCards):
	# 	output = []
	# 	for card in playableCards:
	# 		if card.getRank() == rank:
	# 			output.append(card)
	# 	return output

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
		if not self.isBetterThan(bestHandCard, worstUpCard):
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

	# Returns True iff card is more valuable than otherCard.
	# Value order:
	# 3 > 10 > 2 > A > K > ... > 4
	def isBetterThan(self, card, otherCard):
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

	# Return one of the best cards in a list.
	def bestCardInList(self, cardList):
		bestCard = cardList[0]
		for card in cardList:
			if self.isBetterThan(card, bestCard):
				bestCard = card
		return bestCard

	# Return one of the worst cards in a list.
	def worstCardInList(self, cardList):
		worstCard = cardList[0]
		for card in cardList:
			if self.isBetterThan(worstCard, card):
				worstCard = card
		return worstCard

	# Returns the lowest valued cards in a list.
	def worstCardsInList(self, cardList):
		worstCards = []
		worstCard = cardList[0]
		for card in cardList:
			if worstCard.getRank() == card.getRank():
				worstCards.append(card)
			elif self.isBetterThan(worstCard, card):
				worstCards = [card]
				worstCard = card
		return worstCards

# An Agent that uses basic heuristics, falling back on a 
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
		if not self.isBetterThan(bestHandCard, worstUpCard):
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

	# Returns True iff card is more valuable than otherCard.
	# Value order:
	# 3 > 10 > 2 > A > K > ... > 4
	def isBetterThan(self, card, otherCard):
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

	# Return one of the best cards in a list.
	def bestCardInList(self, cardList):
		bestCard = cardList[0]
		for card in cardList:
			if self.isBetterThan(card, bestCard):
				bestCard = card
		return bestCard

	# Return one of the worst cards in a list.
	def worstCardInList(self, cardList):
		worstCard = cardList[0]
		for card in cardList:
			if isBetterThan(worstCard, card):
				worstCard = card
		return worstCard

	# Returns the lowest valued cards in a list.
	def worstCardsInList(self, cardList):
		worstCards = []
		worstCard = cardList[0]
		for card in cardList:
			if worstCard.getRank() == card.getRank():
				worstCards.append(card)
			elif isBetterThan(worstCard, card):
				worstCards = [card]
				worstCard = card
		return worstCards

	# Returns True iff sevens rule is applicable.
	# Namely, iff cardList contains at least one 6
	# and at least one playable 7.
	def sevensRule(self, cardList, playableCards):
		if self.containsRank(playableCards, 7) and self.containsRank(cardList, 6):
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

	#######################################################
	#######################################################
	# toString Methods for knowledge representations.
	#######################################################
	#######################################################

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

class HumanAgent:

    def __init__(self, agentID):
        self.agentID = agentID
        self.pileRep = util.Stack()        # Internal representation of the pile.
        self.discardPileRep = {}        # Internal representation of the discard pile.
        self.opponentHandRep = {}        # Internal representation of the opponent's hand.

    def getID(self):
        return self.agentID

    def chooseHandCard(self, hand, upCards, playableCards):
        rankToPlay = input("Enter the rank of the card/cards you want to play: ")
        quantityToPlay = input("Enter the number of cards you want to play:" )

        handToPlay = (rankToPlay, quantityToPlay)
        action = self.getActionFromInput(playableCards, quantityToPlay)

        return action

    # Choose the lowest playable cards.
    def chooseUpCard(self, upCards, playableCards):
        rankToPlay = input("Enter the rank of the card/cards you want to play: ")
        quantityToPlay = input("Enter the number of cards you want to play:" )

        handToPlay = (rankToPlay, quantityToPlay)
        action = self.getActionFromInput(playableCards, quantityToPlay)

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
                rankToPlay = input("Enter the rank of the card/cards you want to play: ")
                quantityToPlay = input("Enter the number of cards you want to play:" )
                handToPlay = (rankToPlay, quantityToPlay)
                action = self.getActionFromInput(playableCards, quantityToPlay)
                return action

    # Update knowledge based on percept.
    def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
        return

    # Accepts a tuple as input (rank, quantity) and converts it to an action list
    # returns an empty list if the cards are not available
    def getActionFromInput(self, playableCards, handToPlay):
        action = []
        counter = handToPlay[1] #keeps track of the number of cards to be played
        for card in playAbleCards:
            if (card.getRank() == handToPlay[0]):
                action.append(card)
                counter -= 1
            if counter == 0: break

        if(counter != 0): action = [] #returns an empty(invalid) list if the cards were not available
        return action

# # A Q-learning agent.
# class QLearningAgent:

# 	# Initialize representations, set constants.
# 	def __init__(self, agentID):
# 		self.agentID = agentID
# 		self.type = "LearningAgent"
# 		self.pileRep = util.Stack()		# Internal representation of the pile.
# 		self.discardPileRep = []	# Internal representation of the discard pile.
# 		self.opponentHandRep = []	# Internal representation of the opponent's hand.
# 		self.deckSize = 52 - 18
# 		self.weights = util.Counter() # Stores weights.
# 		self.epsilon = 0.2
# 		self.alpha = 0.1
# 		self.discount = 1
# 		self.featExtractor = fe.featureExtractor()

# 	def getID(self):
# 		return self.agentID

# 	def getType(self):
# 		return self.type

# 	# Look at legal actions and choose best hand cards to play.
# 	def chooseHandCard(self, hand, upCards, playableCards):
# 		return []

# 	# Look at legal actions and choose best up cards to play.
# 	def chooseUpCard(self, upCards, playableCards):
# 		return []

# 	# Trivial; return.
# 	def chooseDownCard(self):
# 		return

# 	# Look at legal actions and choose best move; swap or take first turn.
# 	def chooseSwap(self, hand, upCards, playableCards):
# 		return

# 	# Update knowledge based on percept.
# 	# cardList only given on "PLAY" move.
# 	# agentID only used on "PICKUP" and "PLAY".
# 	# handCard only used on "SWAP", where cardList is an up card.
# 	# On "DRAW", cardList = # of cards drawn.
# 	def updateKnowledge(self, perceptType, agentID=None, cardList=None, handCard=None):
# 		if perceptType == "PICKUP":
# 			while not self.pileRep.isEmpty():
# 				card = self.pileRep.pop()
# 				if card.getRank() == 3:
# 					self.discardPileRep.append(card)
# 				else:
# 					if not agentID == self.getID():
# 						self.opponentHandRep.append(card)
# 		elif perceptType == "DISCARD":
# 			while not self.pileRep.isEmpty():
# 				card = self.pileRep.pop()
# 				self.discardPileRep.append(card)
# 		elif perceptType == "PLAY":
# 			for card in cardList:
# 				if not agentID == self.getID() and card in self.opponentHandRep:
# 					self.opponentHandRep.remove(card)
# 				self.pileRep.push(card)
# 		elif perceptType == "SWAP":
# 			upCard = cardList
# 			handCard = handCard
# 			if not agentID == self.getID():
# 				if handCard in self.opponentHandRep:
# 					self.opponentHandRep.remove(handCard)
# 				self.opponentHandRep.append(upCard)
# 		elif perceptType == "DRAW":
# 			self.deckSize -= cardList
# 		else:
# 			print "INVALID PERCEPT TYPE"
# 		return
		

# 	#######################################################
# 	#######################################################
# 	# LEARNING-SPECIFIC METHODS
# 	#######################################################
# 	#######################################################

#   	def getValue(self, state):
# 	    """
# 	      Returns max_action Q(state,action)
# 	      where the max is over legal actions.  Note that if
# 	      there are no legal actions, which is the case at the
# 	      terminal state, you should return a value of 0.0.
# 	    """
	    
# 	    # All possible actions from state.
# 	    actions = self.getLegalActions(playableCards)
# 	    # Terminal test.
# 	    if not actions:
# 	      return 0.0 
# 	    maxQValue = float("-inf")
# 	    # Find maximum QValue over all actions.
# 	    for action in actions:
# 	      QValue = self.getQValue(state, action)
# 	      if QValue > maxQValue:
# 	        maxQValue = QValue
	          
# 	    return maxQValue

#   	def getPolicy(self, playableCards):
# 	    """
# 	      Compute the best action to take in a state.  Note that if there
# 	      are no legal actions, which is the case at the terminal state,
# 	      you should return None.
# 	    """
# 	    "*** YOUR CODE HERE ***"

# 	    # All possible actions from state.
# 	    actions = self.getLegalActions(playableCards)
# 	    # Terminal test.
# 	    if not actions:
# 	      return None
# 	    maxQValue = float("-inf")
# 	    # Keep a list of actions with equally maximal QValues. 
# 	    maximizingActions = []
# 	    for action in actions:
# 	      QValue = self.getQValue(state, action)
# 	      # If new QValue is strictly greater, list now only contains the new action.
# 	      if QValue > maxQValue:
# 	        maxQValue = QValue
# 	        maximizingActions = [action]
# 	      # If QValue comparison is a tie, add new item to the list.
# 	      elif QValue == maxQValue:
# 	        maximizingActions.append(action)

# 	    # Choose randomly amongst tied actions. Random selection improves performance (value exploration).
# 	    return random.choice(maximizingActions)
    

#   	def getAction(self, playableCards):
# 	    """
# 	      Compute the action to take in the current state.  With
# 	      probability self.epsilon, we should take a random action and
# 	      take the best policy action otherwise.  Note that if there are
# 	      no legal actions, which is the case at the terminal state, you
# 	      should choose None as the action.

# 	      HINT: You might want to use util.flipCoin(prob)
# 	      HINT: To pick randomly from a list, use random.choice(list)
# 	    """
# 	    # Pick Action
# 	    legalActions = self.getLegalActions(playableCards)
# 	    action = None

# 	    "*** YOUR CODE HERE ***"
# 	    explore = util.flipCoin(self.epsilon)
# 	    if explore:
# 	    	action = random.choice(legalActions)
# 	    else: 
# 	    	action = self.getPolicy(playableCards)

# 	    return action

#  	def getQValue(self, state, action):
# 	    """
# 	      Should return Q(state,action) = w * featureVector
# 	      where * is the dotProduct operator
# 	    """

# 	    # Dictionary of (feature->value) pairs.
# 	    featureDict = self.featExtractor.getFeatures(state, action)
# 	    # List of features (keys)
# 	    featureVector = featureDict.keys()

# 	    QValue = 0
# 	    # QValue = sum over all feature values weighted by feature weights.
# 	    for feature in featureVector:
# 	      QValue += self.weights[feature]*featureDict[feature]

# 	    return QValue

#   	def update(self, state, action, nextState, reward):
# 	    """
# 	       Should update your weights based on transition
# 	    """

# 	    # Dictionary of (feature->value) pairs.
# 	    featureDict = self.featExtractor.getFeatures(state, action)
# 	    # List of features (keys)
# 	    featureVector = featureDict.keys()

# 	    # Weight correction value.
# 	    correction = (reward + self.discount*self.getValue(nextState)) - self.getQValue(state, action)

# 	    # Update all weights.
# 	    for feature in featureVector:
# 	      self.weights[feature] += self.alpha*correction*featureDict[feature]

# 	# Returns a list of lists, each inner list representing a legal action.
# 	def getLegalActions(self, playableCards):
# 		actions = []
# 		listsOfRanks = dict()
# 		for rank in range(2, 15):
# 			listsOfRanks[rank] = []
# 		for card in playableCards:
# 			rank = card.getRank()
# 			listsOfRanks[rank].append(card)

# 		for rank in listOfRanks.keys():
# 			rankList = listOfRanks[rank]
# 			for index in range(0, len(rankList)):
# 				tempList = []
# 				for i in range(0, index):
# 					tempList.append(rankList[i])
# 				actions.append(tempList)

# 		return actions









