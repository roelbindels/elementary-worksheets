#!/usr/bin/env python3

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from random import randint

def printHeader(doc,topmargin=770, leftmargin=30):
    doc.drawString(leftmargin,topmargin,"Naam:________________________________")

def printColumns(doc, exercises, columns=2,topmargin=740, bottommargin=50, leftmargin=30):
    number = len(exercises)
    rows = int(number/columns)
    space = int((topmargin-bottommargin)//((number/columns)-1))
    som = []
    for x in range(0,number):
        som.append("{: >3d} {:^3s} {: >3d} {:_<15s}".format(*exercises[x],"="))
        if len(som) == 2:
            regel = "{:<40}{:<40}".format(*som)
            doc.drawString(leftmargin,topmargin - ((x//2)*space),regel)
            som = []

def addPlusExcercises(number, start=1, end=9):
    return generateExerciseList(number,'+', start,end)

def addMinusExcercises(number, start=1, end=9):
    return generateExerciseList(number,'-', start,end)

def addMultipleExcercises(number, start=1, end=9):
    return generateExerciseList(number,'x', start,end)

def addPartExcercises(number, start=1, end=9):
    return generateExerciseList(number,'/', start,end)

def validateOperands(lvalue, rvalue, operator):
    if operator == '-':
        if lvalue < rvalue:
            lvalue, rvalue = rvalue, lvalue
    if operator == '/':
        if rvalue == 0:
            rvalue = 1
    return (lvalue,operator,rvalue)


def generateExerciseList(number, operator, start=1, end=9):
    exercises = []
    for x in range(0,number):
        duplicate = True
        while duplicate:
            if(operator == '/'):
                lvalue = randint(2, 10)
            else:
                lvalue = randint(start, end)
            rvalue = randint(start, end)
            som = validateOperands(rvalue,lvalue,operator)
            if som not in exercises:
                duplicate = False
                exercises.append(som)
    return exercises

def mix(exercises):
    mixed = []
    while (len(exercises) != 0):
        mixed.append( exercises.pop(randint(0, len(exercises)-1)))
    return mixed

if __name__ == "__main__":
    exercises = []
    # exercises += addMultipleExcercises(4)
    # exercises += addMultipleExcercises(10,3,7)
    # exercises += addMultipleExcercises(10,6,9)
    # exercises += addPlusExcercises(5,15,70)
    # exercises += addMinusExcercises(5,15,70)
    exercises += addPartExcercises(30,10,100)

    canvas = Canvas("worksheet.pdf")
    pdfmetrics.registerFont(TTFont("OpenDyslexicMono-Regular", "fonts/OpenDyslexicMono-Regular.ttf"))  
    canvas.setFont('OpenDyslexicMono-Regular', 10)
    printHeader(canvas)
    printColumns(canvas, mix(exercises))
    canvas.save()
