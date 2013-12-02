
# Represents a state of the game as a Q-learner sees it. Represents imperfect 
# information available to the agent.
class State:

	def __init__(self, hand, upCards, oppHandRep, pileRep, discardRep, deckSize):
		self.hand = hand
		self.upCards = upCards
		self.oppHandRep = oppHandRep
		self.pileRep = pileRep
		self.discardRep = discardRep
		self.deckSize = deckSize

	def getHand(self):
		return self.hand

	def getUpCards(self):
		return self.upCards

	def getOppHandRep(self):
		return self.oppHandRep

	def getPileRep(self):
		return self.pileRep

	def getDiscardRep(self):
		return discardRep

	def getDeckSize(self):
		return self.deckSize