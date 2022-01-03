from tkinter import *
import tkinter as tk
from tkinter import ttk
import database as db

BG_COLOR = "#7A797C"
LG_FONT = ("Georgia", 25)

def pos2str(pos):
    return str(pos['Box'])+"."+pos['Row']+str(pos['Column'])

class LookUp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure(bg=BG_COLOR)

        self.frames = {}
        for f in (MainPage, LookUpPage, AddPage, EditPage, DisplayAllPage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self,  font=LG_FONT)
        label.pack(pady=10, padx=10)  

        greeting = Label(self, text="Welcome to team Zoey's Primers Look Up tool",
                        padx=5, pady=3, font=("Georgia", 30))
        greeting.pack(pady=(10,0))

        self.selectedButton = IntVar(self, 999)
        self.descText = StringVar(self, "Choose an option")
        self.pages = [LookUpPage]
        # create frame
        buttonFrame = LabelFrame(self, text="Options",
                                padx=15, pady=25, background=BG_COLOR)
        buttonFrame.pack(padx=25, pady=25)
        # create button and the positions of the button
        buttons = []
        buttons.append(("Look Up", "Search for the position of the primer in the box.", LookUpPage, 0, 1, 1))
        buttons.append(("Add a Primer", "Add a primer. If primer exists, position will be shown.", AddPage, 1, 1, 2))
        buttons.append(("Edit", "Edit the details of the primer.", EditPage, 2, 2, 1))
        buttons.append(("Display All", "See the layout of all the boxes.", DisplayAllPage, 3, 2, 2))

        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        for (text, desc, page, value, row, column) in buttons:
            Radiobutton(buttonFrame, text=text, variable=self.selectedButton, value=value, indicatoron=0, width=15, height=2, font=("Georgia", 20), borderwidth=5, highlightcolor="white",
                            selectcolor="gray25", bg="gray15", fg="snow", command=lambda desc=desc, page = page: self.onSelect(desc, page)).grid(row=row, column=column, padx=15, pady=15)

        # Create description frame
        descFrame = LabelFrame(self, text="Description", padx=5, width=200, height=100,
                            pady=5, background=BG_COLOR, borderwidth=3)
        descFrame.pack(padx=15, pady=(0,25))
        description = Label(descFrame, textvariable=self.descText, padx=5, pady=3, font=(
            "Georgia", 15), background=BG_COLOR, wraplength=400, justify=CENTER).pack(padx=5, pady=5)

        goFrame = Frame(self, padx=5, pady=5, background=BG_COLOR, borderwidth=0)
        goFrame.pack(padx=15,pady=(0,15))
        self.go = Button(goFrame, text="Go", width=10, height=2, font=("Georgia", 20), borderwidth=3, highlightcolor="white", bg="yellow", fg="snow")
        self.go.pack()

    def onSelect(self, desc, page):
        self.descText.set(desc)
        self.go.configure(command= lambda page=page: self.controller.show_frame(page))

class LookUpPage(tk.Frame):
    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        page_label = tk.Label(self, text="Look Up", font=LG_FONT)
        page_label.pack(padx=10, pady=10)
        
        geneFieldVar= StringVar()
        statusText = StringVar()
        
        fieldFrame = Frame(self, padx = 5, pady = 5, background=BG_COLOR, borderwidth=0)
        tk.Label(fieldFrame, text="Gene").pack(side=TOP)
        tk.Entry(fieldFrame, width = 15, textvariable = geneFieldVar).pack()
        fieldFrame.pack(side=TOP)

    
        def submit():
            results = db.lookUp(geneFieldVar.get())
            for primer in results:
                for field in ('id', 'gene', 'species', 'dye', 'placement'):
                    print(field + ": " + primer[field])
                pos = primer['position']
                print('positon' + ": B" + pos2str(pos))
        button = tk.Button(fieldFrame, text = "Submit", command=submit)
        button.pack(side=BOTTOM)

        gobackFrame = Frame(self, padx=5, pady=5, background=BG_COLOR, borderwidth=0)
        gobackFrame.pack(side=BOTTOM, padx=15,pady=(0,15))
        Button(gobackFrame, text="Go Back", width=10, height=2, font=("Georgia", 20), borderwidth=3, highlightcolor="white", bg="yellow", fg="snow", command= lambda: controller.show_frame(MainPage)).pack()

        # def displaytable():
            


    # displaySearch = Label(self,textvariable=statusText, font= ("Georgia",15)).pack(pady=10)


class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        page_label = tk.Label(self, text="Add a Primer", font=LG_FONT)
        page_label.pack(padx=10, pady=10)

        #labels and fills
        formFrame = Frame(self, padx=5, width=200, height=100,
                            pady=5, background=BG_COLOR, borderwidth=3)
        formFrame.pack(side=TOP)
        
        fields = []
        fields.append(("ID", tk.StringVar()))
        fields.append(("Gene", tk.StringVar()))
        fields.append(("Species", tk.StringVar()))
        fields.append(("Dye", tk.StringVar()))
        fields.append(("Placement", tk.StringVar()))
        statusText = StringVar()
        
        for (label, fieldVar) in fields:
            fieldFrame = Frame(formFrame, padx = 5, pady = 5, background=BG_COLOR, borderwidth=0)
            tk.Label(fieldFrame, text=label).pack(side=TOP)
            formEntered = tk.Entry(fieldFrame, width = 15, textvariable = fieldVar)
            formEntered.pack()
            fieldFrame.pack(side=LEFT)
        def submit():
            # if ID is empty, raise a warning
            if len(fields[0][1].get()) == 0:
                statusMessage = "ID is required"
                statusText.set(statusMessage) 
                return

            # try to add the primer
            (success, existing, position) = db.addPrimer(*[f[1].get() for f in fields])

            # if the primer already exists, raise a warning showing the exisiting primer 
            if not success:
                statusMessage = "A Primer with the given id already exists:\n" + str(existing)
                statusText.set(statusMessage)
                fields[0][1].set("")
            # if the primer was successfully added, give the user a position.
            else:
                statusText.set("Primer was successfully added!\nPlease insert into Box" + pos2str(position))
                # clear all the fields
                for (_, fieldVar) in fields:
                    fieldVar.set("")

        button = tk.Button(formFrame, text = "Submit", command=submit)
        button.pack(side=BOTTOM)



        statusLabel = Label(self,textvariable=statusText, font= ("Georgia",15)).pack(pady=10)

        gobackFrame = Frame(self, padx=5, pady=5, background=BG_COLOR, borderwidth=0)
        gobackFrame.pack(side=BOTTOM, padx=15,pady=(0,15))

        Button(gobackFrame, text="Go Back", width=10, height=2, font=("Georgia", 20), borderwidth=3, highlightcolor="white", bg="yellow", fg="snow", command= lambda: controller.show_frame(MainPage)).pack()

class Table(tk.Frame):
    def __init__(self, parent, headings, data):
        tk.Frame.__init__(self, parent)
        tree = ttk.Treeview(self, column =("c1", "c2", "c3", "c4", "c5", "c6","c7"), show = 'headings')
        tree.column("#1", anchor=tk.CENTER)
        tree.heading("#1", text = "#")
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text = "POSITION")
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text = "ID")
        tree.column("#4", anchor=tk.CENTER)
        tree.heading("#4", text = "GENE")
        tree.column("#5", anchor=tk.CENTER)
        tree.heading("#5", text = "SPECIES")
        tree.column("#6", anchor=tk.CENTER)
        tree.heading("#6", text = "DYE")
        tree.column("#7", anchor=tk.CENTER)
        tree.heading("#7", text = "PLACEMENT")
        for i, row in enumerate(data):
            cells = list(row.values())
            cells.insert(0,i+1)
            print(cells)
            cells[1] = pos2str(cells[1])
            tree.insert("", tk.END, values=cells, tag=('odd' if i%2 else 'even'))
        tree.tag_configure('odd', background='#3E3E3E')
        tree.tag_configure('even', background='#2A2A2A')
        tree.pack()
       
class DisplayAllPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        page_label = tk.Label(self, text="Display All", font=LG_FONT)
        page_label.pack(padx=10, pady=10)

        tableFrame = Frame(self, padx=5, width=200, height=200,
                            pady=5, background=BG_COLOR, borderwidth=3)
        tableFrame.pack(side=TOP)
        self.table = Table(tableFrame, [], [])
        self.table.pack()
        def refresh():
            data=db.getAll()
            self.table.destroy()
            self.table = Table(tableFrame, 1, data)
            self.table.pack()
        
        button = tk.Button(self, text = "Refresh", command=refresh)
        button.pack(side=TOP)
   

        gobackFrame = Frame(self, padx=5, pady=5, background=BG_COLOR, borderwidth=0)
        gobackFrame.pack(side=BOTTOM, padx=15,pady=(0,15))

        Button(gobackFrame, text="Go Back", width=10, height=2, font=("Georgia", 20), borderwidth=3, highlightcolor="white", bg="yellow", fg="snow", command= lambda: controller.show_frame(MainPage)).pack()
class EditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        page_label = tk.Label(self, text="Edit", font=LG_FONT)
        page_label.pack(padx=10, pady=10)

        tableFrame = Frame(self, padx=5, width=200, height=200,
                            pady=5, background=BG_COLOR, borderwidth=3)
        gobackFrame = Frame(self, padx=5, pady=5, background=BG_COLOR, borderwidth=0)
        gobackFrame.pack(side=BOTTOM, padx=15,pady=(0,15))

        Button(gobackFrame, text="Go Back", width=10, height=2, font=("Georgia", 20), borderwidth=3, highlightcolor="white", bg="yellow", fg="snow", command= lambda: controller.show_frame(MainPage)).pack()
app = LookUp()
app.mainloop()