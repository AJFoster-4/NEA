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

    #move the raw 2D grid data to the 3D gridData list to hold the values and whether they are correct
    for r in range(9):
        for c in range(9):
            if gridDataRaw[r][c]!=0:
                gridData[r][c][0]=gridDataRaw[r][c]
                gridData[r][c][1]=True
            else:
                gridData[r][c][0]=gridDataRaw[r][c]
                gridData[r][c][1]=None

    #create a copy of the gridDataRaw to pass to be solved
    #this is because the solver modifies gridDataRaw which causes bugs
    empty=[row[:] for row in gridDataRaw]
    solution=solve(empty)

    return gridData, solution


@app.route("/", methods = ["get","post"])
def displayGrid():

    global solution, gridData

    if request.method == "POST":

        action=request.form.get("action")

        #if the user has clicked the solve button, show the solution by replacing all the values in gridData with the corresponding values of the solution
        if action=="showSolution":

            for r in range(9):
                for c in range(9):
                    gridData[r][c][0]=solution[r][c]
                    gridData[r][c][1]=True
        
        #randomly selects a new puzzle

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
        
            #retrieves user's grid with any inputs they've made and turns it into a list

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
                        userGridData[r][c]=(int(cellValue))
                    else:
                        userGridData[r][c]=0
            
            #compare this new list with the solution and assign True or False depending on whether cells are correct
            for r in range(9):
                for c in range(9):
                    if userGridData[r][c]==solution[r][c] and userGridData[r][c]!=0:
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

        #randomly select a medium-difficulty puzzle to use
        num=random.randint(1,3)
        if num==1:
            gridDataRaw=gridM1
        elif num==2:
            gridDataRaw=gridM2
        else:
            gridDataRaw=gridM3


        gridData, solution=setup(gridDataRaw)
        

        
        
    return render_template("interface.html", gridData = gridData)





app.run(debug = True)