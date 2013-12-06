import util

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
		if isinstance(action, tuple):
			if action[0] == None:
				newHand = list(hand)

				#print "Hand: " + util.cardListToString(hand)
				#print "Action : " + util.cardListToString(action[1])
				#print "New Hand: " + util.cardListToString(newHand)


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
			return 0

		else:
			newPileCard = action[0]
			newHand = list(hand)
			for card in action:
				newHand.remove(card)

			numPlayableOn = 0
			for card in newHand:
				if card.isPlayableOn(newPileCard):
					numPlayableOn += 1


		output = dict()
		output["hand-size"] = handSize
		output["opp-hand-size"] = oppHandSize
		output["pile-size"] = pileSize
		output["discard-size"] = discardSize
		output["deck-size"] = deckSize
		output["num-playable-on"] = numPlayableOn
		#output["num-cards-in-action"] = numCardsInAction
		return output

	def maxCardInHand(self, state):
		hand = state.getHand()
		maxCard = util.Card(2, "C")
		for card in hand:
			if card.isPlayableOn(maxCard):
				maxCard = card
		return maxCard