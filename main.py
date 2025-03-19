from puzzleStorage import *
from flask import Flask, render_template, request
import random

app = Flask(__name__)


def findEmpty(bo):
    for r in range(9):
        for c in range(9):
            if bo[r][c]==0:
                return r,c
    return False
#returns row and column of first empty cell


def checkValid(bo, num, pos):
    #check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i]==num and pos[1]!=i:
            return False

    #check column
    for i in range(len(bo)):
        if bo[i][pos[1]]==num and pos[0]!=i:
            return False

    #check 3x3 grid
    box_x=pos[1]//3
    box_y=pos[0]//3

    for i in range(box_y*3, box_y*3+3):
        for j in range(box_x*3, box_x*3+3):
            if bo[i][j]==num and (i, j)!=pos:
                return False

    return True


def solve(bo):
    find=findEmpty(bo)
    if not find:
        return True  #no empty cells left, puzzle solved
    else:
        row, col=find

    for i in range(1, 10):
        if checkValid(bo, i, (row, col)):
            bo[row][col]=i

            if solve(bo):
                #print("boom")
                return bo

            bo[row][col]=0  #reset the cell and backtrack

    return False  #trigger backtracking



solution=None
gridData=None


def setup(gridDataRaw):

    gridData=[
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None]]
    ]

        
    for r in range(9):
        for c in range(9):
            if gridDataRaw[r][c]!=0:
                gridData[c][r][0]=gridDataRaw[r][c]
                gridData[c][r][1]=True
            else:
                gridData[c][r][0]=gridDataRaw[r][c]
                gridData[c][r][1]=None


    empty=[row[:] for row in gridDataRaw]
    solution=solve(empty)

    return gridData, solution


@app.route("/", methods = ["get","post"])
def displayGrid():

    global solution, gridData

    if request.method == "POST":

        action=request.form.get("action")

        if action=="showSolution":

            for r in range(9):
                for c in range(9):
                    gridData[r][c][0]=solution[c][r]
                    gridData[r][c][1]=True
        

        elif action=="e":

            num=random.randint(1,3)
            if num==1:
                gridData, solution=setup(gridE1)
            elif num==2:
                gridData, solution=setup(gridE2)
            else:
                gridData, solution=setup(gridE3)

        elif action=="m":

            num=random.randint(1,3)
            if num==1:
                gridData, solution=setup(gridM1)
            elif num==2:
                gridData, solution=setup(gridM2)
            else:
                gridData, solution=setup(gridM3)

        elif action=="h":

            num=random.randint(1,3)
            if num==1:
                gridData, solution=setup(gridH1)
            elif num==2:
                gridData, solution=setup(gridH2)
            else:
                gridData, solution=setup(gridH3)

        else:
        
            #retrieve form data and turn it into a list

            formData = request.form

            userGridData = [
                    ["","","","","","","","",""],
                    ["","","","","","","","",""],
                    ["","","","","","","","",""],
                    ["","","","","","","","",""],
                    ["","","","","","","","",""],
                    ["","","","","","","","",""],
                    ["","","","","","","","",""],
                    ["","","","","","","","",""],
                    ["","","","","","","","",""]
                ]
            
            for r in range(9):
                for c in range(9):
                    cellName = f"r{r}c{c}"
                    cellValue = formData.get(cellName, "")
                    if cellValue.isdigit():
                        userGridData[c][r]=(int(cellValue))
                    else:
                        userGridData[c][r]=0
            
            #compare this new list with the solution and assign True or False depending on whether cells are correct
            for r in range(9):
                for c in range(9):
                    if userGridData[r][c]==solution[c][r] and userGridData[r][c]!=0:
                        gridData[r][c][0]=userGridData[r][c]
                        gridData[r][c][1]=True
                    elif userGridData[r][c]==0:
                        pass
                    else:
                        gridData[r][c][0]=userGridData[r][c]
                        gridData[r][c][1]=False
        
    else:
        ##Generate a new sudoku
        ##Form this as a grid and send the solution and initial grid
        
        gridDataRaw=None

        num=random.randint(1,3)
        if num==1:
            gridDataRaw=gridM1
        elif num==2:
            gridDataRaw=gridM2
        else:
            gridDataRaw=gridM3


        gridData, solution=setup(gridDataRaw)
        

        
        
    return render_template("solution.html", gridData = gridData)





app.run(debug = True)  



#puzzle "database"









#error log- highlighting function

#added [0] to the end of the gridData calls on lines 23 and 25 in html so the numbers are actually displayed (previously blank cells)
#globalised solution and gridData
#new error- everything highlighted red
#error was on lines 91 and 93, changed c and r around
#added lines 99 and 104- this meant that the grid wasn't reset to its original state after the form was submitted
#new error- when a cell is highlighted red, the number inside is replaced with the correct number (very simple fix on line 104, it was a silly mistake)

#cycle 3- loads of shit getting highligthed wrong when new grids are selected
#this was because I forgot to update solution after having a new grid output

#things to talk about in evaluation:

#re-submitting the form after deleting an incorrect number resets that cell back to the incorrect number entered
#"database" setup is probably dire