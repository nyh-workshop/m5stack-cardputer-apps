import os
import sys
import board
import displayio
import terminalio
import supervisor

from adafruit_display_text import label

Y_OFFSET = 20
Y_ROW_SIZE = 20
MAX_ITEMS_PER_PAGE = 6

BEGIN_LIST = 1
END_LIST = -1

menuItemTextList = ["CapCodeCalc", "ResistorCalc"]
# menuItemTextList = ["HelloWorld", "AnotherApp", "ResistorCalc", "MP3 Player", "SwissArmyKnife", "Weather", "News", "Sports"]
# menuItemTextList = ["HelloWorld", "AnotherApp", "ResistorCalc", "MP3 Player", "SwissArmyKnife", "Weather"]
menuItemTuples = []
menuPageDisplay = []


class SimpleMenu:
    def __init__(self, menuItemTextList):
        # Pages
        self.numOfPages = len(menuItemTextList) // MAX_ITEMS_PER_PAGE
        self.menuPage = 0
        self.menuItemPageTuple = []
       
        # Selector
        self.selectorText = ">"
        self.selectorTextLabel = label.Label(terminalio.FONT, text=self.selectorText, scale=2)
        self.selectorTextLabel.y = Y_OFFSET
        
        self.menuItemTextList = menuItemTextList
        self.menuListGroup = displayio.Group()
        self.menuItemTuples = []
        
        self.GenerateTuplesBasedOnPages(menuItemTextList)
        
        # Menu List Group
        self.textLabels = []
        self.GenerateMenuListGroup()
        self.menuListGroup.append(self.selectorTextLabel)
        
        # Variables for menu selection
        self.menuSelectInPage = 0
        self.menuSelect = 0
        
        # Index number of the items
        self.menuItemIdx = 0
    
    def GenerateMenuListGroup(self):
        for i in range(MAX_ITEMS_PER_PAGE):
            l = label.Label(terminalio.FONT, scale=2)
            self.textLabels.append(l)
            self.menuListGroup.append(l)

    def GetMenuGroup(self):
        return self.menuListGroup
    
    def GetMenuSelectInPageToItemNum(self, menuItemPageTuple):
        return menuItemPageTuple[1] + (menuItemPageTuple[0] * MAX_ITEMS_PER_PAGE)
        
    def GenerateTuplesBasedOnPages(self, menuItemTextList):
        n = 0
        for i in menuItemTextList:
            if(n is not len(menuItemTextList) - 1):
                self.menuItemTuples.append((i, (n // MAX_ITEMS_PER_PAGE), (n % MAX_ITEMS_PER_PAGE), 0))
            else:
                # Insert end of list.
                self.menuItemTuples.append((i, (n // MAX_ITEMS_PER_PAGE), (n % MAX_ITEMS_PER_PAGE), END_LIST))
            n = n + 1
    
    def DrawMenuPage(self, pageNum):
        self.menuSelectInPage = 0
        
        self.menuItemPageTuple = []
        for i in self.menuItemTuples:
            if(i[1] == pageNum):
                self.menuItemPageTuple.append(i)
                
        # Fills that list with specific size and pad with Nones:
        # Ref: https://stackoverflow.com/questions/3438756/some-built-in-to-pad-a-list-in-python
        self.menuItemPageTuple += [None]*(MAX_ITEMS_PER_PAGE-len(self.menuItemPageTuple))
        
        for i in enumerate(self.menuItemPageTuple):
            if (i[1] is None):
                self.textLabels[i[0]].text = ''
            else:
                self.textLabels[i[0]].text = i[1][0]
                self.textLabels[i[0]].x = 20
                self.textLabels[i[0]].y = Y_OFFSET + (i[0] * Y_ROW_SIZE)
            
    def UpdateSelector(self, aInput):
        if(aInput == '.'):
            
            if(self.menuItemPageTuple[self.menuSelectInPage][3] == END_LIST):
                # print(self.menuItemPageTuple[self.menuSelectInPage])
                # print(self.menuSelectInPage, " end of list!")
                return
            else:
                self.menuSelectInPage = self.menuSelectInPage + 1
                
            if(self.menuSelectInPage > (MAX_ITEMS_PER_PAGE - 1)):
                print("next page!")
                self.menuPage = self.menuPage + 1
                self.DrawMenuPage(self.menuPage)
                self.menuSelectInPage = 0
            
            self.selectorTextLabel.y = (self.menuSelectInPage * 20) + Y_OFFSET
                
        elif(aInput == ';'):            
            if(self.menuItemPageTuple[self.menuSelectInPage] is not None):
                self.menuSelectInPage = self.menuSelectInPage - 1
                
            if(self.menuSelectInPage < 0):
                self.menuPage = self.menuPage - 1
                
                if(self.menuPage < 0):
                    self.menuPage = 0
                    self.menuSelectInPage = 0
                else:
                    self.DrawMenuPage(self.menuPage)
                    self.menuSelectInPage = (MAX_ITEMS_PER_PAGE - 1)
                
            if(self.menuItemPageTuple[self.menuSelectInPage] is None):
                print(self.menuSelectInPage, " reached end of list!!")
                return
           
            self.selectorTextLabel.y = (self.menuSelectInPage * 20) + Y_OFFSET
        
        elif(aInput == '\n'):
            print("enter pressed!")
            print("program to run: ", self.menuItemPageTuple[self.menuSelectInPage][0])
            if(self.menuItemPageTuple[self.menuSelectInPage][0] == "CapCodeCalc"):
                supervisor.set_next_code_file('CapCodeCalc.py',reload_on_success=True)
                supervisor.reload()
            
menuObj = SimpleMenu(menuItemTextList)
menuObj.DrawMenuPage(0)
board.DISPLAY.root_group = menuObj.GetMenuGroup()

# Cardputer dir. key layout:
# ';' = up
# '.' = down
# ',' = left
# '/' = right
while True:
   menuObj.UpdateSelector(sys.stdin.read(1))
