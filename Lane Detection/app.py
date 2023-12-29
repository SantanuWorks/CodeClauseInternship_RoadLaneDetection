from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

import LaneDetector

class FileHandler:
    filepath = ""
    def __init__(self, filepath):
        FileHandler.filepath = filepath    

class ResultPage(Frame):

    imagecon = None

    def __init__(self, container, controller):
        super().__init__(container)

        back = Button(self, text="Back", font=("Roboto", 10, "bold"), width=8, pady=3, border=0, relief='sunken', background="lime", foreground="white", command= lambda: self.back(controller, InputPage))
        back.place(relx=0.047, rely=0.05, anchor=CENTER)

        downpane = Frame(self, padx=10, pady=10)
        downpane.config(height = 450, width=950)
        downpane.pack(side="bottom")

        leftpane = Frame(downpane)
        leftpane.config(height = 450, width=470, background = "black")
        leftpane.pack(side="left")

        Frame(downpane, width=10).pack(side="left")

        rightpane = Frame(downpane)
        rightpane.config(height = 450, width=470, background = "black")
        rightpane.pack(side="right")

        ResultPage.leftimg = Label(leftpane, image = None, borderwidth=0)
        ResultPage.leftimg.pack()

        ResultPage.rightimg = Label(rightpane, image = None, borderwidth=0)
        ResultPage.rightimg.pack()

    def LoadResult():

        if FileHandler.filepath != "":
            raw_input = LaneDetector.get_img(FileHandler.filepath)
            raw_output = LaneDetector.LaneDetector(raw_input)

            input = Image.open(FileHandler.filepath)
            input = input.resize((470, 450))
            input = ImageTk.PhotoImage(input)

            output = Image.fromarray(raw_output, 'RGB')
            output.save('media/results/result.png')
            output = Image.open("media/results/result.png")
            output = output.resize((470, 450))
            output = ImageTk.PhotoImage(output)
            
            ResultPage.leftimg.config(image=input)
            ResultPage.leftimg.dontloseit = input

            ResultPage.rightimg.config(image=output)
            ResultPage.rightimg.dontloseit = output

    def back(self, controller, page):
        controller.switchpage(page)

class InputPage(Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        downpane = Frame(self)
        downpane.config(height = 520, width=970, background = "#d400ff")
        downpane.pack(anchor = "w")

        welcon = Label(downpane, text = "Lane Detector", font=("Console", 22, "bold"), borderwidth=0, background = "#d400ff", foreground="white")
        welcon.place(relx=0.5, rely=0.45, anchor=CENTER)

        filebutton = Button(downpane, text = "Select Picture", font=("Roboto", 12, "bold"), width=15, pady=5, border=0, relief='sunken', background="lime", foreground="white", command= lambda: self.select_file(controller, ResultPage)) 
        filebutton.place(relx=0.5, rely=0.55, anchor=CENTER)

    def get_file(self):
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a picture")
        if ".jpg" in filename or ".png" in filename:
            return filename
        return ""
    
    def select_file(self, controller, page):
        filepath = self.get_file()
        if filepath != "":
            FileHandler(filepath)
            ResultPage.LoadResult()
            controller.switchpage(page)
    
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Lane Detector")
        self.geometry("970x520")
        self.resizable(False, False)

        container = Frame(self)
        container.pack(side = "bottom", fill = "both")
        self.pages = {}

        for PageClass in (InputPage, ResultPage):
            page = PageClass(container, self)
            self.pages[PageClass] = page 
            page.grid(column=0, row=0, sticky="nsew")
        self.switchpage(InputPage)

    # switch pages
    def switchpage(self, pageclass):
        page = self.pages[pageclass]
        page.tkraise()

if __name__ == "__main__":
    LaneDetectorApp = App()
    LaneDetectorApp.mainloop()