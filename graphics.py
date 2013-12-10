#!/usr/bin/env python      

from Tkinter import *       
import GameBoard as gb
import util
import game
import experiment as ex

class Graphics(Frame):
    
    def __init__(self, root=Tk()):
        Frame.__init__(self,root)
        self.root = root
        self.root.grid()
        self.root.title('Scheisskopf')
        self.theGameBoard = None
        self.theAgents = []
        self.cardImages = {}
        self.children = []
        self.upsAndDowns = []
        self.makeGraphics()

        #### test new approach for making and erasing labels ####
        self.backImage = PhotoImage(file="Deck1.gif")
        self.cardLabels = {}
        self.cardLabels["back"] = Label(self.root, image=self.backImage)
        for suit in ["C","S","D","H"]:
            for i in range(13):
                rank = i + 1
                if rank == 1: rank = "A"
                elif rank == 11: rank = "J"
                elif rank == 12: rank = "Q"
                elif rank == 13: rank = "K"
                else: rank = str(rank)
                cardName = suit + rank
                cardPhoto = PhotoImage(file=cardName + ".gif")
                self.cardLabels[cardName] = Label(self.root, image=cardPhoto)
                
        

        """
        # Store card pictures in dict() for later use
        for suit in ["C","S","D","H"]:
            for i in range(13):
                rank = i + 1
                if rank == 1: rank = "A"
                elif rank == 11: rank = "J"
                elif rank == 12: rank = "Q"
                elif rank == 13: rank = "K"
                else: rank = str(rank)
                cardName = suit + rank
                self.cardImages[cardName] = PhotoImage(file=cardName + ".gif")
        """     


    # use this to update graphics with the new gameboard
    def setGameBoard(self, newGameBoard):
        self.theGameBoard = newGameBoard

    # provide graphics with the correct agents to get access to hands
    def setAgents(self, newAgents):
        for i in range(len(newAgents)):
            self.theAgents.append(newAgents[i])

    # erases the gameboard
    def deleteChildren(self):
        for child in self.children:
            child.destroy()
            
    # erase up and down cards
    def deleteUpsAndDowns(self):
        for card in self.upsAndDowns:
            card.destroy()
    
    #### DO THIS INSTEAD OF COMPLETELY REDOING ENTIRE GAMEBOARD EVERY TIME ####
    def initiateGraphics(self):

        # set up card positions
        self.pad_x = 5
        self.pad_y = 10
        self.decks_row = 2
        self.play_col = 6
        self.decks_offset = 4
        self.up_down_col = 5
        self.up_down_offset = 1
        self.hand_row = self.decks_row + 3

        # computer up and down card labels
        for i in range(2):
            if i == 1: 
                text = Label(self.root,text='Down cards:')
                text.grid(row=i,column=self.up_down_col-1,padx=self.pad_x,pady=self.pad_y)
            else: 
                text = Label(self.root,text='Up cards:')
                text.grid(row=i,column=self.up_down_col-1,padx=self.pad_x,pady=self.pad_y)
            


            """    
            for n in range(3):
                label = Label(self.root,image=self.backImage)
                label.grid(row=i,column=self.up_down_col+n,padx=self.pad_x,pady=self.pad_y)
            """



    # clears the board to display only pictures of the back of the cards 
    def makeGraphics(self):
        # get image on back of cards
        #self.imageDir = "/home/cs-students/14jsd1/Desktop/finalProject-master/Cards_gif/"
        #self.backImage = PhotoImage(file="Deck1.gif")
        


        """
        # set up card positions
        self.pad_x = 5
        self.pad_y = 10
        self.decks_row = 2
        self.play_col = 6
        self.decks_offset = 4
        self.up_down_col = 5
        self.up_down_offset = 1
        self.hand_row = self.decks_row + 3

        # computer up and down cards
        for i in range(2):
            if i == 1: 
                text = Label(self.root,text='Down cards:')
                text.grid(row=i,column=self.up_down_col-1,padx=self.pad_x,pady=self.pad_y)
            else: 
                text = Label(self.root,text='Up cards:')
                text.grid(row=i,column=self.up_down_col-1,padx=self.pad_x,pady=self.pad_y)
            for n in range(3):
                label = Label(self.root,image=self.backImage)
                label.grid(row=i,column=self.up_down_col+n,padx=self.pad_x,pady=self.pad_y)
        """
        
        # discard pile
        discardText = Label(self.root, text='Discard:')
        discardText.grid(row=self.decks_row,column=self.play_col-self.decks_offset-1,padx=self.pad_x,pady=self.pad_y)
        discardP = Label(self.root, image=self.backImage)
        discardP.grid(row=self.decks_row,column=self.play_col-self.decks_offset,padx=self.pad_x,pady=self.pad_y)

        # playing pile
        playingText = Label(self.root, text='Play card:')
        playingText.grid(row=self.decks_row,column=self.play_col-1,padx=self.pad_x,pady=self.pad_y)
        playingP = Label(self.root, image=self.backImage)
        playingP.grid(row=self.decks_row,column=self.play_col,padx=self.pad_x,pady=self.pad_y)

        #pick up deck
        pickUpText = Label(self.root,text='Pick up:')
        pickUpText.grid(row=self.decks_row,column=self.play_col+self.decks_offset-1,padx=self.pad_x,pady=self.pad_y)
        pickUpP = Label(self.root, image=self.backImage)
        pickUpP.grid(row=self.decks_row,column=self.play_col+self.decks_offset,padx=self.pad_x,pady=self.pad_y)

        # player up and down cards
        for i in range(2):
            if i == 0: 
                text = Label(self.root,text='Down cards:')
                text.grid(row=self.decks_row+self.up_down_offset+i,column=self.up_down_col-1,padx=self.pad_x,pady=self.pad_y)
            else: 
                text = Label(self.root,text='Up cards:')
                text.grid(row=self.decks_row+self.up_down_offset+i,column=self.up_down_col-1,padx=self.pad_x,pady=self.pad_y)
            for n in range(3):
                label = Label(self.root, image=self.backImage)
                self.upsAndDowns.append(label)
                label.grid(row=self.decks_row+self.up_down_offset+i,column=self.up_down_col+n,padx=self.pad_x,pady=self.pad_y)

        # player hand    
        for n in range(13):
            label = Label(self.root, image=self.backImage)
            label.grid(row=self.hand_row,column=n,padx=self.pad_x,pady=self.pad_y)

    # updates the graphical representation of the gameboard
    def updateGraphics(self):

        self.deleteChildren()
        self.deleteUpsAndDowns()

        # reset gameboard before updating 
        self.makeGraphics()

        self.deleteUpsAndDowns()

        # get all player-viewable information to display
        topOfPile = self.theGameBoard.peekPile()
        topOfDiscard = self.theGameBoard.peekDiscard()
        playerHand = self.theGameBoard.viewHand(self.theAgents[0])
        playerUps = self.theGameBoard.viewUpCards(self.theAgents[0])
        computerUps = self.theGameBoard.viewUpCards(self.theAgents[1])
        playerDowns = self.theGameBoard.viewDownCards(self.theAgents[0])
        computerDowns = self.theGameBoard.viewDownCards(self.theAgents[1])

        # display player's hand
        cardsHere = {}
        for col in range(13):
            cardsHere[col] = (False,0)
        for card in playerHand:
            cardImage = self.cardImages[card.toString()]
            playerCard = Label(self.root, image=cardImage)
            self.children.append(playerCard)
            if cardsHere[card.getRank()-2][0]:
                yPadding = self.pad_y + 3*(self.pad_y * cardsHere[card.getRank()-2][1])
                playerCard.grid(row=self.hand_row,column=card.getRank()-2,padx=self.pad_x,pady=(yPadding,self.pad_y))                
                numCards = cardsHere[card.getRank() - 2][1] + 1
                cardsHere[card.getRank() - 2] = (True, numCards)
            else:
                numCards = cardsHere[card.getRank() - 2][1] + 1
                cardsHere[card.getRank() - 2] = (True, numCards)
                playerCard.grid(row=self.hand_row,column=card.getRank()-2,padx=self.pad_x,pady=self.pad_y)

        # display top card of pile
        if not topOfPile == None:
            cardImage = self.cardImages[topOfPile.toString()]
            topPileCard = Label(self.root, image=cardImage)
            topPileCard.grid(row=self.decks_row,column=self.play_col,padx=self.pad_x,pady=self.pad_y)

        # display top card of discard pile
        if not topOfDiscard == None:
            cardImage = self.cardImages[topOfDiscard.toString()]
            topDiscardCard = Label(self.root, image=cardImage)
            topDiscardCard.grid(row=self.decks_row,column=self.play_col-self.decks_offset,padx=self.pad_x,pady=self.pad_y)

        # display player's up cards
        for i in range(len(playerUps)):
            cardImage = self.cardImages[playerUps[i].toString()]
            upCard = Label(self.root, image=cardImage)
            self.upsAndDowns.append(upCard)
            upCard.grid(row=self.decks_row+self.up_down_offset+1,column=self.up_down_col+i,padx=self.pad_x,pady=self.pad_y)

        # display computer up cards
        for i in range(len(computerUps)):
            cardImage = self.cardImages[computerUps[i].toString()]
            upCard = Label(self.root, image=cardImage)
            self.upsAndDowns.append(upCard)
            upCard.grid(row=self.decks_row-self.up_down_offset-1,column=self.up_down_col+i,padx=self.pad_x,pady=self.pad_y)

        # re-display player's down cards
        for i in range(len(playerDowns)):
            downCard = Label(self.root, image=self.backImage)
            downCard.grid(row=self.decks_row+self.up_down_offset,column=self.up_down_col+i,padx=self.pad_x,pady=self.pad_y)
 
        # re-display computer's down cards
        for i in range(len(computerDowns)):
            downCard = Label(self.root, image=self.backImage)
            downCard.grid(row=self.decks_row-self.up_down_offset,column=self.up_down_col+i,padx=self.pad_x,pady=self.pad_y)
            
