import util

# Extracts a feature vector from a Q-learner's state representation.
class featureExtractor:

	def __init__(self):
		return

	# Returns a dict from features to counts.
	def getFeatures(self, state, action):
		hand = state.getHand()
		handSize = len(hand)
		upCards = state.getUpCards()
		oppHandRep = state.getOppHandRep()
		oppHandSize = len(oppHandRep)
		pileRep = state.getPileRep()
		pileSize = pileRep.size()
		discardRep = state.getDiscardRep()
		discardSize = len(discardRep)
		deckSize = state.getDeckSize()
		numCardsInAction = len(action)

		# Compute the number of hand cards playable on the newly played card(s).

		if action == "DOWNCARD":
			numPlayableOn = 0

		elif hand == []:
			numPlayableOn = 0

		elif isinstance(action, tuple):
			if action[0] == None:
				newHand = list(hand)

			for card in action[1]:
				newHand.remove(card)

			newPileCard = action[1][0]
			if newPileCard == 10 or newPileCard == 3:
				numPlayableOn = len(newHand)
			else:
				numPlayableOn = 0
				for card in newHand:
					if card.isPlayableOn(newPileCard):
						numPlayableOn += 1

					else:
						numPlayableOn = len(hand)
		elif action == []:
			numPlayableOn = 0
		else:
			newPileCard = action[0]
			newHand = list(hand)
			for card in action:
				newHand.remove(card)

			numPlayableOn = 0
			for card in newHand:
				if card.isPlayableOn(newPileCard):
					numPlayableOn += 1
			
		# FEATURES:
		output = dict()
		# Size of hand.
		output["hand-size"] = handSize

		# Size of opponent's hand.
		output["opp-hand-size"] = oppHandSize

		# Size of pile.
		output["pile-size"] = pileSize

		# Size of discard pile.
		output["discard-size"] = discardSize

		# Size of deck.
		output["deck-size"] = deckSize

		# Number of cards in hand playable on pile after action.
		output["num-playable-on"] = numPlayableOn
		return output

	def maxCardInHand(self, state):
		hand = state.getHand()
		maxCard = util.Card(2, "C")
		for card in hand:
			if card.isPlayableOn(maxCard):
				maxCard = card
		return maxCard
