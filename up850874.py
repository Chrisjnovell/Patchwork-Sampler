# Chris Novell, UP850874
# Python Coursework

from graphics import *
import time, math
from random import random

def main():
    size, colours = inputs()
    win, location, ordercolour = createwindow(size, colours)
    drawpatches(win, size, colours)
    # Advanced feature
    while True:
        location, ordercolour = swappatch(win, size, location, ordercolour)

def inputs():
    correct = False
    while not correct:
        size = eval(input("Enter the patchwork size: "))
        if size == 5 or size == 7 or size == 9 or size == 11:
            break
        else:
            print("Valid sizes are: 5, 7, 9, or 11")
    colours = []
    validcolours = ["red", "green", "blue", "magenta", "cyan", "orange", "brown", "pink"]
    for i in range(3):
        while not correct:
            colour = input("Enter a colour: ")
            if colour in validcolours and colour not in colours:
                colours.append(colour)
                break
            elif colour in colours:
                print("This colour has already been entered")
            else:
                print("Valid colours are:")
                for vcolour in validcolours:
                    if vcolour == "pink": print("and", vcolour)
                    else: print(vcolour + ", ", end="")
    return size, colours

def createwindow(size, colours):
    win = GraphWin("Coursework", size * 100, size * 100 )
    drawrectangle(win,Point(0, 0) , Point(size * 100, size * 100), "white", "white")
    location = []
    for i in range(size):
        for j in range(size):
            if j < 3 and i >= size - 3:
                location.append("f")
            else:
                location.append("p")
    ordercolour = []
    for i in range(size**2):
        ordercolour.append(colours[i % 3])
    return win, location, ordercolour

def drawpatches(win, size, colours):
    # i --> height, j --> width
    for i in range(size):
        for j in range(size):
            if i >= size - 3 and j <= 2:
                finalpatch(win, Point(j * 100, i * 100), colours[(j + (size * i))% 3])
            else:
                penpatch(win, Point(j * 100, i * 100), colours[(j + (size * i))% 3])

def finalpatch(win, topleft, colour):
    x = topleft.getX()
    y = topleft.getY()
    # i --> height, j --> width
    for i in range(5):
        if i == 1 or i == 3: fillcolour = "white"
        else: fillcolour = colour
        for j in range(5):
            centre = Point(x + 10 + (j * 20), y + 10 + (i * 20))
            drawcircle(win, centre, 10, fillcolour, colour)

def penpatch(win, topleft, colour):
    x = topleft.getX()
    y = topleft.getY()
    # Draw background colours
    for i in range(10):
        if i % 2 == 1:
            drawrectangle(win, Point(x, y + (i * 10)), Point(x + 100, y + (i * 10) + 10), colour, colour)
        else:
            drawrectangle(win, Point(x, y + (i * 10)), Point(x + 100, y + (i * 10) + 10), "white", "white")
    # Draw triangles on top: i --> height, j --> width
    for i in range(10):
        if i % 2 == 1: fillcolour = "white"
        else: fillcolour = colour
        for j in range(5):
            p1 = Point(x + (j * 20), y + (i * 10) + 10) # Far left point
            p2 = Point(x + (j * 20) + 10, y + (i * 10)) # Top point
            p3 = Point(x + (j * 20) + 20, y + (i * 10) + 10) # Far right point
            drawtriangle(win, p1, p2, p3, fillcolour, fillcolour)

def drawcircle(win, centre, radius, fillcolour, edgecolour):
    circle = Circle(centre, radius)
    circle.setFill(fillcolour)
    circle.setOutline(edgecolour)
    circle.draw(win)

def drawrectangle(win, p1, p2, fillcolour, edgecolour):
    rect = Rectangle(p1, p2)
    rect.setFill(fillcolour)
    rect.setOutline(edgecolour)
    rect.draw(win)

def drawtriangle(win, p1, p2, p3, fillcolour, edgecolour):
    triangle = Polygon(p1, p2, p3)
    triangle.setFill(fillcolour)
    triangle.setOutline(edgecolour)
    triangle.draw(win)

def swappatch(win, size, location, ordercolour):
    # First click
    click1 = win.getMouse()
    x1= int(click1.getX()/100) + 1
    y1 = int(click1.getY()/100) + 1
    patch1 = str(x1) + str(y1) + location[size * (y1 - 1) + x1 - 1] + ordercolour[size * (y1 - 1) + x1 - 1]
    topleft1 = Point((x1 - 1) * 100, (y1 - 1) * 100)
    # Second click
    click2 = win.getMouse()
    x2= int(click2.getX()/100) + 1
    y2 = int(click2.getY()/100) + 1
    patch2 = str(x2) + str(y2) + location[size * (y2 - 1) + x2 - 1] + ordercolour[size * (y2 - 1) + x2 - 1]
    topleft2 = Point((x2 - 1) * 100, (y2 - 1) * 100)
    # Clicks in the same patch
    if patch1 == patch2:
        drawrectangle(win, topleft1, Point(x1 * 100, y1 * 100), "white", "white")
        if patch1[2] == "p":
            location[size * (y1 - 1) + x1 - 1] = "f"
            finalpatch(win, topleft1, patch1[3:])
        else:
            location[size * (y2 - 1) + x2 - 1] = "p"
            penpatch(win, topleft2, patch2[3:])
    # Clicks in different patches
    else:
        location[size * (y2 - 1) + x2 - 1] = patch1[2] # Swap patch types in location list
        location[size * (y1 - 1) + x1 - 1] = patch2[2]
        ordercolour[size * (y1 - 1) + x1 - 1] = patch2[3:] # Swap colours in ordercolour list
        ordercolour[size * (y2 - 1) + x2 - 1] = patch1[3:]
        drawrectangle(win, Point((x1 - 1) * 100, (y1 - 1) * 100), Point(x1 * 100, y1 * 100), "white", "white") # Creates a blank background for redraw
        drawrectangle(win, Point((x2 - 1) * 100, (y2 - 1) * 100), Point(x2 * 100, y2 * 100), "white", "white")
        # Draw the new patch using new lists
        if patch2[2] == "p":
            penpatch(win, topleft1, patch2[3:])
        else:
            finalpatch(win, topleft1, patch2[3:])
        if patch1[2] == "p":
            penpatch(win, topleft2, patch1[3:])
        else:
            finalpatch(win, topleft2, patch1[3:])
    return location, ordercolour

main()
