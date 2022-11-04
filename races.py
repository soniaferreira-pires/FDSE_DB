import pwinput
import psycopg2
import tkinter as tk

# -------------------------------------------- CONNECT TO  DATABASE ---------------------------------------------------#

# connected = False
# while not connected:

#     username = input('Type your database username: ')
#     password = pwinput.pwinput(prompt='Type your database password: ', mask='*')

#     try:
#         con = psycopg2.connect(
#             database=username,  # your database is the same as your username
#             user=username,  # your username
#             password=password,  # your password
#             host="dbm.fe.up.pt",  # the database host
#             port="5433",
#             options='-c search_path=public') # use the schema you want to connect to
#         connected = True

#     except psycopg2.OperationalError:
#         print("You're not connected to FEUP VPN or inputed wrong credentials.")
#     else:
#         print("You successfully connected to the database.")
#     finally:
#         continue


# ---------------------------------------------------------------------------------------------------#
# ----------------------------------------- INTERFACE------------------------------------------------#
# ---------------------------------------------------------------------------------------------------#

from tkinter import *
window=Tk()


# ----------------------------------------- FUNCTIONS BUTTONS ------------------------------------------------#






#MENU BAR 

def search_runner():
    hide_all_frames()
    search_runner_lframe.pack(fill="both", expand=1)

    r_name = Label(search_runner_lframe, text = "Runner name:").place(x = 30,y = 50)
    rname_en = Entry(search_runner_lframe).place(x = 120,y = 50)  
    submitbtn = Button(search_runner_lframe, text = "Submit",activebackground = "red", 
                        activeforeground = "blue").place(x = 30, y = 170)

    search_runner_lframe.mainloop()


def get_values_event(e):
    values_eid = e.eid_en.get()
    return

def search_event(e):
    hide_all_frames()
    search_events_lframe.pack(fill="both", expand=1)

    e_id = Label(search_events_lframe, text = "Event ID:").place(x = 30,y = 20)
    
    number1 = tk.StringVar()
    e.eid_en = Entry(search_events_lframe, textvariable=number1 ).place(x = 120,y = 20)
    e_name = Label(search_events_lframe, text = "Event name:").place(x = 30,y = 50)
    ename_en = Entry(search_events_lframe).place(x = 120,y = 50)  

    submitbtn = Button(search_events_lframe, text = "Submit",activebackground = "red", 
                        activeforeground = "blue").place(x = 30, y = 170)
    msg = Message(search_events_lframe, text = "result from BD")  


    T = tk.Text(search_events_lframe, height=10, width=100).place(x = 30,y = 250)
    #T.pack()
    T.insert(tk.END, "test test test")
    
    search_events_lframe.mainloop()




#hide remain frames 
def hide_all_frames():
    search_runner_lframe.pack_forget()
    search_events_lframe.pack_forget()

# def clear_frame():
#    for widgets in search_events_lframe.winfo_children():
#       widgets.destroy()
# ----------------------------------------- MENU BAR ------------------------------------------------#
menubar = Menu(window)  

#Menu 1
new = Menu(menubar, tearoff=0) 
new.add_command(label="Runner")  
new.add_command(label="Team")  
new.add_command(label="Event")  
new.add_command(label="Event Type") 
new.add_command(label="Age Class") 
new.add_command(label="Participation Details")  
new.add_separator()  
new.add_command(label="Exit", command=window.quit)  
menubar.add_cascade(label="New", menu=new)  

#Menu 2
search = Menu(menubar, tearoff=0)  
search.add_command(label="Runner", command = search_runner)  
search.add_command(label="Events", command= search_event)  
search.add_command(label="Teams")    
menubar.add_cascade(label="Search", menu=search)  
help = Menu(menubar, tearoff=0)  

#Menu 3
help.add_command(label="About")  
menubar.add_cascade(label="Help", menu=help)  
  
window.config(menu=menubar)  


lblcenter=Label(window, text="Races Events - Management Studio", fg='light gray', font=("Helvetica", 22))
lblcenter.place(relx = 0.5, rely = 0.5, anchor = 'center')

lblmecd=Label(window, text="MECD - Databases @2022", fg='light gray', font=("Helvetica", 10, "bold"))
lblmecd.place(relx = 1.0, rely = 1.0, anchor = 'se')




# ----------------------------------------- CREATE FRAMES ------------------------------------------------#
search_runner_lframe = LabelFrame(window, width=850, height=550, text='search a runner')
search_events_lframe = LabelFrame(window, width=900, height=600,text='search a event')


window.title('Races Events - Management Studio')
window.geometry("900x600+10+20")
window.mainloop()


