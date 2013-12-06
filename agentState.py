

# Represents a state of the game as a Q-learner sees it. Represents imperfect 
# information available to the agent.
class State:

	def __init__(self, hand, upCards, playableCards, oppHandRep, pileRep, discardRep, deckSize, terminal):
		self.hand = hand
		self.upCards = upCards
		self.playableCards = playableCards
		self.oppHandRep = oppHandRep
		self.pileRep = pileRep
		self.discardRep = discardRep
		self.deckSize = deckSize
		self.terminal = terminal

	def getHand(self):
		return self.hand

	def getUpCards(self):
		return self.upCards

	def getPlayableCards(self):
		return self.playableCards

	def getOppHandRep(self):
		return self.oppHandRep

	def getPileRep(self):
		return self.pileRep

	def getDiscardRep(self):
		return self.discardRep

	def getDeckSize(self):
		return self.deckSize

	def isTerminal(self):
		return self.terminal