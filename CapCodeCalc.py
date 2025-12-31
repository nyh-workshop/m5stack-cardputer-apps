# For the CardPuter use only! :D
import sys
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

dispGroup = displayio.Group()
inputTextLabel = label.Label(terminalio.FONT, text='', scale=4)
inputTextLabel.x = 24
inputTextLabel.y = 80
scriptTitle = label.Label(terminalio.FONT, text='CAPACITOR CODE CALC', scale=2)
scriptTitle.x = 5
scriptTitle.y = 20
resultTextLabel = label.Label(terminalio.FONT, text='_____ pf\n_____ nf\n_____ uf', scale=2)
resultTextLabel.x = 120
resultTextLabel.y = 50
rect = Rect(10, 40, 100, 80, fill=None, outline=0xFFFFFF, stroke=0x02)

dispGroup.append(scriptTitle)
dispGroup.append(inputTextLabel)
dispGroup.append(resultTextLabel)
dispGroup.append(rect)

board.DISPLAY.root_group = dispGroup

tempInput = ''
tempInputThreeChrList = ['', '', '']

while True:
    error = False
    for i in range(3):
        tempInputThreeChrList[i] = sys.stdin.read(1)
        resultTextLabel.text = '_____ pf\n_____ nf\n_____ uf'
        if(tempInputThreeChrList[i].isdigit() is False):
            # Wipes screen and restart when wrong input:
            # print("error!")
            tempInputThreeChrList = ['', '', '']
            inputTextLabel.text = ''
            error = True
            break
        else:
            inputTextLabel.text = ''.join(tempInputThreeChrList)
    
    if error is not True:
        capacitorCodeString = ''.join(tempInputThreeChrList)
        firstTwoDigitsFromLeftStr = capacitorCodeString[0:2]
        value = float(firstTwoDigitsFromLeftStr) * (10e-12) * pow(10, int(capacitorCodeString[-1]))
        
        pfValue = value/10e-12
        nfValue = value/10e-9
        ufValue = value/10e-6
        
        resultTextLabel.text = '{:.4}pf\n{:.4}nf\n{:.4}uf'.format(pfValue, nfValue, ufValue)    
        print(inputTextLabel.text)
        print(value)
    
    

    
