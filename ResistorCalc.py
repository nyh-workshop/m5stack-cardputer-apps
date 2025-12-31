# For the CardPuter use only! :D
import sys
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.triangle import Triangle

dispGroup = displayio.Group()

# Resistor Color codes: https://people.duke.edu/~ng46/topics/color-code.htm
colorLookup = [0x000000, 0x996633, 0xff0000, 0xff9900, 0xffff00, 0x00ff00, 0x0000ff, 0xff00ff, 0xcccccc, 0xffffff]

colorToleranceLookup = [0xbec7c7, 0xd6c372]

colors = [0,0,0]
toleranceValue = 0

RESISTOR_RECT_OFFSET_X = 30

# Title
scriptTitle = label.Label(terminalio.FONT, text='RESISTOR CODE CALC', scale=2)
scriptTitle.x = 5
scriptTitle.y = 20
# Resistor Rectangle
resistorRect = Rect(10 + RESISTOR_RECT_OFFSET_X, 40, 150, 40, fill=0x000000, outline=0xFFFFFF, stroke=0x02)
# Resistor Color Bars
resistorColor0Rect = Rect(30 + RESISTOR_RECT_OFFSET_X, 40, 15, 40, fill=None, outline=0xFFFFFF, stroke=0x01)
resistorColor1Rect = Rect(60 + RESISTOR_RECT_OFFSET_X, 40, 15, 40, fill=None, outline=0xFFFFFF, stroke=0x01)
resistorColor2Rect = Rect(90 + RESISTOR_RECT_OFFSET_X, 40, 15, 40, fill=None, outline=0xFFFFFF, stroke=0x01)
resistorColor3Rect = Rect(120 + RESISTOR_RECT_OFFSET_X, 40, 15, 40, fill=None, outline=0xFFFFFF, stroke=0x01)
# Caret
caretLabel = label.Label(terminalio.FONT, text='^', scale=3)
caretLabel.x = 30 + RESISTOR_RECT_OFFSET_X
caretLabel.y = 100
# Resistor Value
resistorValueLabel = label.Label(terminalio.FONT, text='', scale=3)
resistorValueLabel.x = 40
resistorValueLabel.y = 110

dispGroup.append(scriptTitle)
dispGroup.append(resistorRect)
dispGroup.append(resistorColor0Rect)
dispGroup.append(resistorColor1Rect)
dispGroup.append(resistorColor2Rect)
dispGroup.append(resistorColor3Rect)
dispGroup.append(caretLabel)
dispGroup.append(resistorValueLabel)

board.DISPLAY.root_group = dispGroup

colorBarSelect = 0
toleranceColorSelect = 0
colorSelect = 0

colorBarSelectLookup = [resistorColor0Rect, resistorColor1Rect, resistorColor2Rect, resistorColor3Rect]

resistorColor3Rect.fill = colorToleranceLookup[toleranceColorSelect]

# Repeating code! Will optimize later!
while True:
    
    FirstTwoDigits = colors[1] + (colors[0]*10)
    Multiplier = pow(10, colors[2])
    ResistorValue = FirstTwoDigits * Multiplier
    print(ResistorValue)
    # print(toleranceColorSelect)
    resistorValueStr = ''
    toleranceValueStr = ''
    
    if(colors[2] in range(0,2)):
        resistorValueStr = '{}'.format(ResistorValue)
    elif(colors[2] in range(2,5)):
        resistorValueStr = '{}k'.format(ResistorValue / 1000)
    elif(colors[2] in range(5,8)):
        resistorValueStr = '{}M'.format(ResistorValue / 1000000)
    elif(colors[2] in range(8,10)):
        resistorValueStr = '{}G'.format(ResistorValue / 1000000000)
        
    if(toleranceColorSelect == 0):
        toleranceValueStr = "10%"
    else:
        toleranceValueStr = "5%"        
    
    resistorValueLabel.text = "{} {}".format(resistorValueStr, toleranceValueStr)
    
    aInput = sys.stdin.read(1)
    if(aInput == ','):
        colorBarSelect = colorBarSelect - 1
        colorBarSelect = colorBarSelect % 4
        caretLabel.x = colorBarSelect * 30 + RESISTOR_RECT_OFFSET_X * 2
    elif(aInput == '/'):
        colorBarSelect = colorBarSelect + 1
        colorBarSelect = colorBarSelect % 4
        caretLabel.x = colorBarSelect * 30 + RESISTOR_RECT_OFFSET_X * 2
    elif(aInput == ';'):
        if(colorBarSelect is not 3):
            colorSelect = colorSelect + 1
            colorSelect = colorSelect % 10        
            colorBarSelectLookup[colorBarSelect].fill = colorLookup[colorSelect]
            colors[colorBarSelect] = colorSelect
        else:
            toleranceColorSelect = toleranceColorSelect + 1
            toleranceColorSelect = toleranceColorSelect % 2
            colorBarSelectLookup[colorBarSelect].fill = colorToleranceLookup[toleranceColorSelect]
    elif(aInput == '.'):
        if(colorBarSelect is not 3):
            colorSelect = colorSelect - 1
            colorSelect = colorSelect % 10 
            colorBarSelectLookup[colorBarSelect].fill = colorLookup[colorSelect]
            colors[colorBarSelect] = colorSelect
        else:
            toleranceColorSelect = toleranceColorSelect - 1
            toleranceColorSelect = toleranceColorSelect % 2
            colorBarSelectLookup[colorBarSelect].fill = colorToleranceLookup[toleranceColorSelect]
            
    
