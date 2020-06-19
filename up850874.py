# Chris Novell, UP850874
# Python Coursework

from graphics import *
import time, math
from random import random

def main():
    size, colours = inputs()
    win, location, orderColour = createWindow(size, colours)
    drawPatches(win, size, colours)
    # Advanced feature
    while True:
        location, orderColour = swapPatch(win, size, location, orderColour)

def inputs():
    correct = False
    while not correct:
        size = eval(input("Enter the patchwork size: "))
        if size == 5 or size == 7 or size == 9 or size == 11:
            break
        else:
            print("Valid sizes are: 5, 7, 9, or 11")
    colours = []
    validColours = ["red", "green", "blue", "magenta", "cyan", "orange", "brown", "pink"]
    for i in range(3):
        while not correct:
            colour = input("Enter a colour: ")
            if colour in validColours and colour not in colours:
                colours.append(colour)
                break
            elif colour in colours:
                print("This colour has already been entered")
            else:
                print("Valid colours are:")
                for vcolour in validColours:
                    if vcolour == "pink": print("and", vcolour)
                    else: print(vcolour + ", ", end="")
    return size, colours

def createWindow(size, colours):
    win = GraphWin("Coursework", size * 100, size * 100 )
    drawRectangle(win,Point(0, 0) , Point(size * 100, size * 100), "white", "white")
    location = []
    for i in range(size):
        for j in range(size):
            if j < 3 and i >= size - 3:
                location.append("f")
            else:
                location.append("p")
    orderColour = []
    for i in range(size**2):
        orderColour.append(colours[i % 3])
    return win, location, orderColour

def drawPatches(win, size, colours):
    # i --> height, j --> width
    for i in range(size):
        for j in range(size):
            if i >= size - 3 and j <= 2:
                finalPatch(win, Point(j * 100, i * 100), colours[(j + (size * i))% 3])
            else:
                penPatch(win, Point(j * 100, i * 100), colours[(j + (size * i))% 3])

def finalPatch(win, topLeft, colour):
    x = topLeft.getX()
    y = topLeft.getY()
    # i --> height, j --> width
    for i in range(5):
        if i == 1 or i == 3: fillColour = "white"
        else: fillColour = colour
        for j in range(5):
            centre = Point(x + 10 + (j * 20), y + 10 + (i * 20))
            drawCircle(win, centre, 10, fillColour, colour)

def penPatch(win, topLeft, colour):
    x = topLeft.getX()
    y = topLeft.getY()
    # Draw background colours
    for i in range(10):
        if i % 2 == 1:
            drawRectangle(win, Point(x, y + (i * 10)), Point(x + 100, y + (i * 10) + 10), colour, colour)
        else:
            drawRectangle(win, Point(x, y + (i * 10)), Point(x + 100, y + (i * 10) + 10), "white", "white")
    # Draw triangles on top: i --> height, j --> width
    for i in range(10):
        if i % 2 == 1: fillColour = "white"
        else: fillColour = colour
        for j in range(5):
            p1 = Point(x + (j * 20), y + (i * 10) + 10) # Far left point
            p2 = Point(x + (j * 20) + 10, y + (i * 10)) # Top point
            p3 = Point(x + (j * 20) + 20, y + (i * 10) + 10) # Far right point
            drawtriangle(win, p1, p2, p3, fillColour, fillColour)

def drawCircle(win, centre, radius, fillColour, edgeColour):
    circle = Circle(centre, radius)
    circle.setFill(fillColour)
    circle.setOutline(edgeColour)
    circle.draw(win)

def drawRectangle(win, p1, p2, fillColour, edgeColour):
    rect = Rectangle(p1, p2)
    rect.setFill(fillColour)
    rect.setOutline(edgeColour)
    rect.draw(win)

def drawTriangle(win, p1, p2, p3, fillColour, edgeColour):
    triangle = Polygon(p1, p2, p3)
    triangle.setFill(fillColour)
    triangle.setOutline(edgeColour)
    triangle.draw(win)

def swapPatch(win, size, location, orderColour):
    # First click
    click1 = win.getMouse()
    x1= int(click1.getX()/100) + 1
    y1 = int(click1.getY()/100) + 1
    patch1 = str(x1) + str(y1) + location[size * (y1 - 1) + x1 - 1] + orderColour[size * (y1 - 1) + x1 - 1]
    topLeft1 = Point((x1 - 1) * 100, (y1 - 1) * 100)
    # Second click
    click2 = win.getMouse()
    x2= int(click2.getX()/100) + 1
    y2 = int(click2.getY()/100) + 1
    patch2 = str(x2) + str(y2) + location[size * (y2 - 1) + x2 - 1] + orderColour[size * (y2 - 1) + x2 - 1]
    topLeft2 = Point((x2 - 1) * 100, (y2 - 1) * 100)
    # Clicks in the same patch
    if patch1 == patch2:
        drawRectangle(win, topLeft1, Point(x1 * 100, y1 * 100), "white", "white")
        if patch1[2] == "p":
            location[size * (y1 - 1) + x1 - 1] = "f"
            finalPatch(win, topLeft1, patch1[3:])
        else:
            location[size * (y2 - 1) + x2 - 1] = "p"
            penPatch(win, topLeft2, patch2[3:])
    # Clicks in different patches
    else:
        location[size * (y2 - 1) + x2 - 1] = patch1[2] # Swap patch types in location list
        location[size * (y1 - 1) + x1 - 1] = patch2[2]
        orderColour[size * (y1 - 1) + x1 - 1] = patch2[3:] # Swap colours in ordercolour list
        orderColour[size * (y2 - 1) + x2 - 1] = patch1[3:]
        drawRectangle(win, Point((x1 - 1) * 100, (y1 - 1) * 100), Point(x1 * 100, y1 * 100), "white", "white") # Creates a blank background for redraw
        drawRectangle(win, Point((x2 - 1) * 100, (y2 - 1) * 100), Point(x2 * 100, y2 * 100), "white", "white")
        # Draw the new patch using new lists
        if patch2[2] == "p":
            penPatch(win, topLeft1, patch2[3:])
        else:
            finalPatch(win, topLeft1, patch2[3:])
        if patch1[2] == "p":
            penPatch(win, topLeft2, patch1[3:])
        else:
            finalPatch(win, topLeft2, patch1[3:])
    return location, orderColour

main()
