class featureExtractor:

	def __init__(self):
		return

	# Returns a dict from features to counts.
	def getFeatures(self, state, action):
		hand = state.getHand()
		handSize = len(hand)

		upCards = state.getUpCards()
		oppHandRep = state.getOppHandRep()

		pileRep = state.getPileRep()
		pileSize = pileRep.size()

		discardRep = state.getDiscardRep()
		discardSize = len(discardRep)

		deckSize = state.getDeckSize()

		output = dict()
		output["hand-size"] = handSize
		output["pile-size"] = pileSize
		output["discard-size"] = discardSize
		output["deck-size"] = deckSize
		return output