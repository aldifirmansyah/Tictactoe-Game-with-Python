from tkinter import *
from tkinter import messagebox

class BoardGame:

    def __init__(self):
        self.history = str()
        self.landingPage()
        
    def landingPage(self):
        self.formPage = Tk()
        self.formPage.title("New Game")
        self.formPage.configure(background = "white")

        # create menu bar
        menubar = Menu(self.formPage)
        menubar = Menu(menubar, tearoff = 0)
        menubar.add_command(label = "History", command=self.showHistory)
        menubar.add_command(label = "Exit", command=lambda : self.formPage.destroy())
        self.formPage.config(menu = menubar)

        # create form
        Label(self.formPage, text = "Height:", bg = "white", font = "Helvetica 10 bold").grid(row = 1, column = 1, pady = 10)
        v1 = StringVar()
        Entry(self.formPage, textvariable = v1, font = "Helvetica 8 bold").grid(row = 1, column = 2, padx = 10, pady = 10, ipadx = 10, ipady = 4)

        Label(self.formPage, text = "Width:", bg = "white", font = "Helvetica 10 bold").grid(row = 2, column = 1, pady = 10)
        v2 = StringVar()
        Entry(self.formPage, textvariable = v2, font = "Helvetica 8 bold").grid(row = 2, column = 2, padx = 10, pady = 10, ipadx = 10, ipady = 4)
        
        Label(self.formPage, text = "Combo:", bg = "white", font = "Helvetica 10 bold").grid(row = 3, column = 1, pady = 10)
        v3 = StringVar()
        Entry(self.formPage, textvariable = v3, font = "Helvetica 8 bold").grid(row = 3, column = 2, padx = 10, pady = 10, ipadx = 10, ipady = 4)

        # submit button
        Button(self.formPage, text = "submit", command=lambda : self.submit(v1.get(), v2.get(), v3.get())).grid(row = 4, column = 1)

        self.formPage.mainloop()

    def submit(self, height, width, combo):
        if not height.isdigit() or not width.isdigit() or not combo.isdigit():
            messagebox.showinfo("Error", "Input must be filled with number!")
            return

        height, width, combo = int(height), int(width), int(combo)
        
        if combo > height or combo > width:
            messagebox.showinfo("Error", "Combo should not bigger than height or width!")
            return

        self.formPage.destroy()
        self.startGame(height, width, combo)

    def startGame(self, height, width, combo):
        self.player = 1
        self.totalTurn = 1
        self.combo = combo
        self.aHeight = height
        self.aWidth = width
        
        self.mainPage = Tk()
        self.mainPage.title("Board Game")
        self.mainPage.configure(background = "white")

        # title
        Label(self.mainPage, text = "BOARD GAME", bg = "white", font = "Helvetica 20 bold").grid(row = 1, column = 1)

        # create menu bar
        menubar = Menu(self.mainPage)
        menubar = Menu(menubar, tearoff = 0)
        menubar.add_command(label = "History", command=self.showHistory)
        menubar.add_command(label = "Exit", command=lambda : self.mainPage.destroy())
        self.mainPage.config(menu = menubar)
        
        # create canvas
        self.canvas = Canvas(self.mainPage)
        self.canvas['width'] = 100 * width
        self.canvas['height'] = 100 * height
        self.coordinates = list()
        for h in range(height):
            self.coordinates.append([0] * width)
            for w in range(width):
                self.canvas.create_rectangle(w * 100, h * 100, (w+1) * 100, (h+1) * 100)
        self.canvas.bind("<Button-1>", self.onClick)      
        self.canvas.grid(row = 2, column = 1)

    def onClick(self, event):
        try:
            width = event.x // 100
            height = event.y // 100
            print("{}  {}".format(width,height))

            if self.coordinates[height][width] != 0:
                return

            if self.player == 1:
                self.canvas.create_oval(width * 100 + 10, height * 100 + 10, (width+1) * 100 - 10, (height+1) * 100 - 10)
                self.coordinates[height][width] = self.player
            else:
                self.canvas.create_line(width * 100 + 10, height * 100 + 10, (width+1) * 100 - 10, (height+1) * 100 - 10)
                self.canvas.create_line(width * 100 + 90, height * 100 + 10, (width+1) * 100 - 90, (height+1) * 100 - 10)
                self.coordinates[height][width] = self.player

            # check combo
            isWin = self.comboCheck(width, height)
            if isWin:
                self.endGame()

            if self.totalTurn == self.aWidth * self.aHeight:
                self.tieGame()
            
            self.player = 2 if self.player == 1 else 1
            self.totalTurn += 1
                
            print(self.coordinates)

        except Exception as error:
            print(error)
            pass
        
    def comboCheck(self, width, height):
        isWin = self.checkVertical(width, height)
        if isWin:
            return True
        
        isWin = self.checkHorizontal(width, height)
        if isWin:
            return True

        isWin = self.checkDiagonal1(width, height)
        if isWin:
            return True

        isWin = self.checkDiagonal2(width, height)
        if isWin:
            return True
    
    def checkVertical(self, width, height):
        counterUp, counterDown = 0,0

        # count downside
        heightTemp = height + 1
        while heightTemp < self.aHeight:
            if self.coordinates[heightTemp][width] == self.player:
                counterDown += 1
                heightTemp += 1
            else:
                break

        # count upside
        heightTemp = height - 1
        while heightTemp >= 0:
            if self.coordinates[heightTemp][width] == self.player:
                counterUp += 1
                heightTemp -= 1
            else:
                break

        return (counterUp + counterDown + 1) >= self.combo

    def checkHorizontal(self, width, height):
        counterLeft, counterRight = 0,0

        # count leftside
        widthTemp = width - 1
        while widthTemp >= 0:
            if self.coordinates[height][widthTemp] == self.player:
                counterLeft += 1
                widthTemp -= 1
            else:
                break

        # count rightside
        widthTemp = width + 1
        while widthTemp < self.aWidth:
            if self.coordinates[height][widthTemp] == self.player:
                counterRight += 1
                widthTemp += 1
            else:
                break

        return (counterLeft + counterRight + 1) >= self.combo

    def checkDiagonal1(self, width, height):
        counterLeftUp, counterRightDown = 0,0

        #counter leftupside
        widthTemp = width - 1
        heightTemp = height - 1
        while widthTemp >= 0 and heightTemp >= 0:
            if self.coordinates[heightTemp][widthTemp] == self.player:
                counterLeftUp += 1
                widthTemp -= 1
                heightTemp -= 1
            else:
                break

        #counter rightdownside
        widthTemp = width + 1
        heightTemp = height + 1
        while widthTemp < self.aWidth and heightTemp < self.aHeight:
            if self.coordinates[heightTemp][widthTemp] == self.player:
                counterRightDown += 1
                widthTemp += 1
                heightTemp += 1
            else:
                break
        print("leftup {} rightdown {}".format(counterLeftUp, counterRightDown))
        return(counterLeftUp + counterRightDown + 1) >= self.combo

    def checkDiagonal2(self, width, height):
        counterLeftDown, counterRightUp = 0,0

        # counter leftdownside
        widthTemp = width - 1
        heightTemp = height + 1
        while widthTemp >= 0 and heightTemp < self.aHeight:
            if self.coordinates[heightTemp][widthTemp] == self.player:
                counterLeftDown += 1
                widthTemp -= 1
                heightTemp += 1
            else:
                break

        # counter rightupside
        widthTemp = width + 1
        heightTemp = height - 1
        while widthTemp < self.aWidth and heightTemp >= 0:
            if self.coordinates[heightTemp][widthTemp] == self.player:
                counterRightUp += 1
                widthTemp += 1
                heightTemp -= 1
            else:
                break

        return(counterLeftDown + counterRightUp + 1) >= self.combo

    def endGame(self):
        self.history += "Player {} win in a {}x{} game with {} combo at turns {}\n".format(self.player, self.aWidth, self.aHeight, self.combo, self.totalTurn)
        self.canvas.unbind("<Button-1>")
        messagebox.showinfo("Game Finished", "Player {} win the game!".format(self.player))

        self.mainPage.destroy()
        self.landingPage()

    def tieGame(self):
        self.history += "Tie game in {}x{} with {} combo\n".format(self.aWidth, self.aHeight, self.combo)
        messagebox.showinfo("Game Finished", "Tie!")

        self.mainPage.destroy()
        self.landingPage()
    
    def showHistory(self):
        messagebox.showinfo("Game History", self.history)


BoardGame()
