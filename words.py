#!/usr/bin/env python3

from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from random import randint
import re

def printHeader(doc,topmargin=770, leftmargin=30):
    doc.drawString(leftmargin,topmargin,"Naam:________________________________")

def printColumns(doc, items, columns=2,topmargin=740, bottommargin=50, leftmargin=30):
    number = len(items)
    space = int((topmargin-bottommargin)//((number/columns)-1))
    row = []
    for x in range(0,number):
        row.append("{:<8s} {:s}".format(*items[x]))
        if len(row) == columns:
            doc.drawString(
                leftmargin,topmargin - ((x//2)*space),
                "{:<40}{:<40}".format(*row)
                )
            row = []

def createDoc(items):
    canvas = Canvas("worksheet.pdf")
    pdfmetrics.registerFont(TTFont("OpenDyslexicMono-Regular", "fonts/OpenDyslexicMono-Regular.ttf"))  
    canvas.setFont('OpenDyslexicMono-Regular', 10)
    printHeader(canvas)
    printColumns(canvas, mix(items))
    canvas.save()

def compileReplaceRegex(query):
    if query == 'o':
        regex = re.compile(r'((?<!o)o(?![oeu]))')
    elif query == 'oo':
        regex = re.compile(r'((?<!o)oo(?![oeu]))')
    elif query == 'a':
        regex = re.compile(r'((?<!a)a(?![au]))')
    elif query == 'aa':
        regex = re.compile(r'((?<!a)aa(?![au]))')
    elif query == 'e':
        regex = re.compile(r'((?<![oie])e(?![eiu]))')
    elif query == 'ee':
        regex = re.compile(r'((?<![oie])ee(?![eiu]))')
    elif query == 'u':
        regex = re.compile(r'((?<![auoe])u(?![iu]))')
    elif query == 'uu':
        regex = re.compile(r'((?<![auoe])uu(?![iu]))')
    return regex

def compileFilterRegex(query):
    if query == 'o':
        regex = re.compile(r'^[^o]*o[^oeu]+\w+')
    elif query == 'oo':
        regex = re.compile(r'^[^o]*oo[^oeu]+\w+')
    elif query == 'a':
        regex = re.compile(r'^[^a]*a[^au]+\w+')
    elif query == 'aa':
        regex = re.compile(r'^[^a]*aa[^au]+\w+')
    elif query == 'e':
        regex = re.compile(r'^[^oie]*e[^eiu]+\w+')
    elif query == 'ee':
        regex = re.compile(r'^[^oie]*ee[^eiu]+\w+')
    elif query == 'u':
        regex = re.compile(r'^[^aoue]*u[^iu]+\w+')
    elif query == 'uu':
        regex = re.compile(r'^[^auoe]*uu[^iu]+\w+')
    return regex

def getDescription(query):
    if query == 'o' or query == 'oo':
        descr = "(o/oo)"
    elif query == 'a' or query == 'aa':
        descr = "(a/aa)"
    elif query == 'e' or query == 'ee':
        descr = "(e/ee)"
    elif query == 'u' or query == 'uu':
        descr = "(u/uu)"
    return descr

def filterExerciseList(query, items):
    regex = compileFilterRegex(query)

    selected_items = list(filter(regex.search, items))
    return selected_items

def replaceWithBlancs(query, items, blanc = '_', number = 3):
    regex = compileReplaceRegex(query)
    processed_items = []

    for item in items:
        processed_items.append((getDescription(query),regex.sub(blanc * number,item)))
    return processed_items

def getWordsFromFiles(filenames):
    lines = []
    for filename in filenames:
        with open(filename) as f:
            lines += f.read().splitlines()
    return lines

def pickRandomitems(number, items):
    selected = []
    
    for x in range(0,number):
        selected.append( items.pop(randint(0, len(items)-1)))
    return selected

def generateExerciseList(query, number):
    items = replaceWithBlancs(query,
        pickRandomitems(number,
            filterExerciseList(query,
                getWordsFromFiles([
                    'words/nl_NL/taalactief/grp4.txt',
                    'words/nl_NL/taalactief/grp5.txt',
                    'words/nl_NL/taalopmaat/grp5.txt'
                    ]))))
    return items


def mix(items):
    mixed = []
    while (len(items) != 0):
        mixed.append( items.pop(randint(0, len(items)-1)))
    return mixed

if __name__ == "__main__":
    exercises = []
    exercises += generateExerciseList('oo',5)
    exercises += generateExerciseList('o',5)
    exercises += generateExerciseList('aa',5)
    exercises += generateExerciseList('a',5)
    exercises += generateExerciseList('ee',5)
    exercises += generateExerciseList('e',5)
    exercises += generateExerciseList('uu',5)
    exercises += generateExerciseList('u',5)

    createDoc(exercises)