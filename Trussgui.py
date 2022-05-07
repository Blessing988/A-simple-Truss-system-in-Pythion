
#Importing relevant libraries and functions
import tkinter as tk
from tkinter import ttk
from numpy import sqrt, transpose, linalg, array, dot

from PythonTruss import Node, Member, Analysis #Importing the classes used in the hard-coding script

win = tk.Tk()  # Creating a window
win.resizable(False, False)  # making the win non-resizable
win.geometry("200x200")  # setting the geometry or size of the window
win.state("zoomed")  # making it a fullscreen

# A function which shows the three frames used


def show_frame(frames):
    frames.tkraise()

win.rowconfigure(0, weight = 1 )  #setting the weight of the columns
win.columnconfigure(0, weight = 1) #setting the weight of the rows

main_frame = tk.Frame(win, bg = "yellow") #Creating the main frame
second_frame = tk.Frame(win, bg = "pink")  #Creating the second frame
third_frame = tk.Frame(win)  #Creating the third frame
main_frame.grid_propagate(False)

# Griding the three frames
for frame in (main_frame, second_frame, third_frame):
    frame.grid(row =0, column = 0, sticky = "nsew")


nodes_num = tk.StringVar()  #Creating a textvariable for number of nodes
member_num = tk.StringVar()  #Creating a textvariable for number of members

nodes_label = ttk.Label(main_frame, text="Enter the number of nodes: ")
nodes_label.grid(row=0, column=0, sticky="w")

nodes_entry = ttk.Entry(main_frame, width=12, textvariable=nodes_num)
nodes_entry.grid(row=0, column=1)

member_label = ttk.Label(main_frame, text="Enter the number of members: ")
member_label.grid(row=0, column=2)
member_entry = ttk.Entry(main_frame, width=12, textvariable=member_num)
member_entry.grid(row=0, column=3)

#lists to store all the entries relating to the nodes
x_entries = []
y_entries = []
Sx_entries = []
Sy_entries = []
fx_entries = []
fy_entries = []

#lists to store the entries of the start and end of nodes of members
start_entries = []
end_entries = []

#node coordinates to plot
xplotpts = []
yplotpts = []

#member coordinates to plot
mem_xplots = []
mem_yplots = [ ]

#A list of values relating to the nodes
xcor = []   #x-coordinates of the node
ycor = []   #y-coordinates of the nodes
Sx = []     #Horizontal reaction
Sy = []     #Vertical reaction
fx = []     #Horizontal load
fy = []     #Vertical load

#Start and end nodes values of members
start_nodes = []
end_nodes = []

#Dictionaries holding all the
nodes_dict = {}
member_dict = {}
reactions_dict = {}

def func():
    nodes = int(nodes_num.get())
    member = int(member_num.get())
    nodes_entry.destroy()
    member_entry.destroy()
    t = 'Enter "1" if there is a vertical or horizontal reaction at a node\nEnter "0" if there is no vertical or horizontal reaction at a node'
    infolbl = ttk.Label(main_frame, text=t, font='Helvetica 10 bold')
    infolbl.grid(row=1, column=0, columnspan=3, rowspan=2)

    #Creating LabelFrames to contain the values of Node id, x , y, Sy, Sx, fx, fy
    node_labelFrame = ttk.LabelFrame(main_frame, text="Node id")
    node_labelFrame.grid(row=3, column=0)
    x_labelFrame = ttk.LabelFrame(main_frame, text="x")
    x_labelFrame.grid(row=3, column=1)
    y_labelFrame = ttk.LabelFrame(main_frame, text="y")
    y_labelFrame.grid(row=3, column=2)
    Sy_labelFrame = ttk.LabelFrame(main_frame, text="Vertical Reaction")
    Sy_labelFrame.grid(row=3, column=3)
    Sx_labelFrame = ttk.LabelFrame(main_frame, text="Horizontal Reaction")
    Sx_labelFrame.grid(row=3, column=4)
    fx_labelFrame = ttk.LabelFrame(main_frame, text="Horizontal Load")
    fx_labelFrame.grid(row=3, column=5)
    fy_labelFrame = ttk.LabelFrame(main_frame, text="Vertical Load")
    fy_labelFrame.grid(row=3, column=6)

    #Creating entries and appending them to a list
    for i in range(nodes):
        id_label = ttk.Label(node_labelFrame, text="Node " + str(i + 1))
        id_label.grid(row=i, column=0, padx = 1, pady = 1)
        x_entry = ttk.Entry(x_labelFrame, width=12)
        x_entries.append(x_entry)
        x_entry.grid(row=i, column=1)

        y_entry = ttk.Entry(y_labelFrame, width=12)
        y_entries.append(y_entry)
        y_entry.grid(row=i, column=2)

        Sy_entry = ttk.Entry(Sy_labelFrame, width=12)
        Sy_entries.append(Sy_entry)
        Sy_entry.grid(row=i, column=3)
        Sy_entry.insert(0, 0)

        Sx_entry = ttk.Entry(Sx_labelFrame, width=12)
        Sx_entries.append(Sx_entry)
        Sx_entry.grid(row=i, column=4)
        Sx_entry.insert(0, 0)

        fx_entry = ttk.Entry(fx_labelFrame, width=12)
        fx_entries.append(fx_entry)
        fx_entry.grid(row=i, column=5)
        fx_entry.insert(0, 0)

        fy_entry = ttk.Entry(fy_labelFrame, width=12)
        fy_entries.append(fy_entry)
        fy_entry.grid(row=i, column=6)
        fy_entry.insert(0, 0)

    def func2():

        #Retrieving the values from the entries
        for entry in range(nodes):
            xcor.append(float(x_entries[entry].get()))
            ycor.append(float(y_entries[entry].get()))
            Sy.append(float(Sy_entries[entry].get()))
            Sx.append(float(Sx_entries[entry].get()))
            fx.append(float(fx_entries[entry].get()))
            fy.append(float(fy_entries[entry].get()))


        for i in range(nodes):
            nodes_dict[str(i + 1)] = Node(str(i + 1), xcor[i], ycor[i], Sy[i], Sx[i], fx[i], fy[i])  #Making the values available to the Node class
            reactions_dict[str(i+1)] = (Sy[i], Sx[i])


        #Creating labelframes to containing the member id, start node of members, end nodes of members
        member_labelFrame = ttk.LabelFrame(main_frame, text="Member id")
        member_labelFrame.grid(row=3, column=7)
        start_node_labelFrame = ttk.LabelFrame(main_frame, text="Start Node Number")
        start_node_labelFrame.grid(row=3, column=8)
        end_node_labelFrame = ttk.LabelFrame(main_frame, text="End Node Number")
        end_node_labelFrame.grid(row=3, column=9)

        #Creating entries and appending them to a list
        for i in range(member):
            member_id = ttk.Label(member_labelFrame, text="Member " + str(i + 1))
            member_id.grid(row=i, column=0, padx = 1, pady = 1)
            start_entry = ttk.Entry(start_node_labelFrame, width=12)
            start_entries.append(start_entry)
            start_entry.grid(row=i, column=1)

            end_entry = ttk.Entry(end_node_labelFrame, width=12)
            end_entries.append(end_entry)
            end_entry.grid(row=i, column=2)



        def func3():
            #Retreieving the values of the start and end nodes of members from the entries
            for entry in range(member):
                start_nodes.append(start_entries[entry].get())
                end_nodes.append(end_entries[entry].get())

            #Making the values accessible by the Member class
            for i in range(member):
                member_dict[str(i + 1)] = Member(str(i + 1), nodes_dict[start_nodes[i]], nodes_dict[end_nodes[i]])

            #Calculating forces in members and reactions at nodes
            g = Analysis()
            g.calculate()

            def func4():

                second_frame.grid_propagate()
                #Creating a Canvas
                plotcanvs = tk.Canvas(second_frame, bg='pink', highlightthickness=0, height=720, width=1280)

                tk.Canvas(second_frame, bg='pink', highlightthickness=0)
                plotcanvs.grid(row=0, column=0, sticky='nsew')

                plotcanvs.update()
                w = plotcanvs.winfo_width() - 30
                h = plotcanvs.winfo_height() - 30

                ############## Code to plot the nodes ###########
                xmax, ymax, xmin, ymin = max(xcor), max(ycor), min(xcor), min(ycor)
                if xmin <= 0:
                    alpax = w / xmax - xmin
                else:
                    alpax = w / xmax
                if ymin <= 0:
                    alpay = h / ymax - ymin
                else:
                    alpay = h / ymax
                for i in range(len(xcor)):
                    x, y = int(xcor[i]), int(ycor[i])
                    vert = (h - alpay * 0.8 * y) - h / 9
                    yplotpts.append(vert)
                    hori = (alpax * 0.8 * x) + w / 8
                    xplotpts.append(hori)
                    x1, y1, x2, y2 = hori - 6, vert - 6, hori + 6, vert + 6
                    plotcanvs.create_oval(x1, y1, x2, y2, width=2, fill='blue', tags='nodes')
                    t = 'N' + str(i + 1)
                    plotcanvs.create_text(x2 + 10, y2 + 10, text=t, font=('Areal 10 bold'), tags='nodenum')

                ############## Code to plot the members ###########

                for i in range(member):
                    sn = int(start_nodes[i])
                    en = int(end_nodes[i])
                    x1 = xplotpts[sn - 1]
                    y1 = yplotpts[sn - 1]
                    x2 = xplotpts[en - 1]
                    y2 = yplotpts[en - 1]
                    plotcanvs.create_line(x1, y1, x2, y2, width=3, tags='elements')
                    t = 'M' + str(i + 1)
                    plotcanvs.create_text(((x1 + x2) / 2) + 15, ((y1 + y2) / 2) + 15, text=t, font='Arial 10 bold',
                                          tags='elnum')


                show_frame(second_frame)
                second_frame_btn = tk.Button(second_frame, text="Show Forces in Members",
                                             command=lambda: show_frame(third_frame), bg = "saddlebrown")
                second_frame_btn.grid(row=1, column=0)
            func4()

            #Creating Frames and Label Frames  which stores the state of members(whether they are in tension and compression)
            member_force_frame = ttk.Frame(third_frame)
            member_force_frame.grid(row=0, column=0)
            member_id_forces = ttk.LabelFrame(member_force_frame, text="Members")
            member_id_forces.grid(row=0, column=0, sticky="nsew")
            member_value_forces = ttk.LabelFrame(member_force_frame, text="Forces in Members (kN)")
            member_value_forces.grid(row=0, column=1, sticky="nsew")
            state_of_member_frame = ttk.LabelFrame(member_force_frame, text = "State of Members")
            state_of_member_frame.grid(row = 0, column =2, sticky = "nsew")

            
            Total_Eq_Matrix = transpose(Analysis.Equilibrium_Matrix)
            inverse = linalg.inv(Total_Eq_Matrix)
            P = array(Analysis.Matrix)
            result = inverse.dot(P)

            ##### Code to check whether the forces are in tension or compression ####
            for i in range(member):
                lbl_id = ttk.Label(member_id_forces, text=str(i + 1), font='Courier 12')
                lbl_id.grid(row=i, column=0, sticky="nsew")
                mem_forces = ttk.Label(member_value_forces, text=str(abs(round(result[i][0], 3))), font='Courier 12')
                mem_forces.grid(row=i, column=1, sticky="nsew")

                if result[i][0] < 0:
                    state = ttk.Label(state_of_member_frame, text = "Tension", font = 'Courier 12')
                    state.grid(row = i, column = 2)
                elif result[i][0] > 0:
                    state = ttk.Label(state_of_member_frame, text="Compression", font='Courier 12')
                    state.grid(row=i, column=2)
                else:
                    state = ttk.Label(state_of_member_frame, text="Zero force member", font='Courier 12')
                    state.grid(row=i, column=2)

            frame_rxns = ttk.Frame(third_frame)
            frame_rxns.grid(row = 0, column = 1)
            reaction_frame = ttk.LabelFrame(frame_rxns, text = "Reactions at supports")
            reaction_frame.grid(row = 0, column =0)

            for r in range(len(result[member:])):
                ttk.Label(reaction_frame, text = str(result[member:][r][0]), font = "Courier 12").grid(row = r, column = 0)


            main_frame_btn = tk.Button(main_frame, text = "Next Page", command = lambda : show_frame(second_frame), bg = "orchid3")
            main_frame_btn.grid(row = 4, column = 9)

        button_3 = tk.Button(main_frame, text="Plot Truss", command=  func3, bg = "red")
        button_3.grid(row=4, column=7, columnspan = 2)

    button2 = ttk.Button(main_frame, text="OK", command=func2)
    button2.grid(row=4, column=0)

show_frame(main_frame) #Showing the mainframe

third_frame_btn = tk.Button(third_frame, text = "Back to Main Page",  command= lambda : show_frame(main_frame), bg = "DarkOrange1")
third_frame_btn.grid(row= 1, column = 0)
button_1 = ttk.Button(main_frame, text="OK", command=func)
button_1.grid(row=0, column=4)
win.mainloop()