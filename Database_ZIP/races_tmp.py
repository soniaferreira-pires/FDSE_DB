import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import W, E, N, S
from tkinter import messagebox
# from tkinter import Menu
import psycopg2
import pwinput
import datetime


#-------------------------------------------- CONNECT TO  DATABASE ---------------------------------------------------#
connected = False
while not connected:

    # username = input('Type your database username: ')
    # password = pwinput.pwinput(prompt='Type your database password: ', mask='*')

    try:
        con = psycopg2.connect(
            database="fced_sonia_ferreira",  # your database is the same as your username #############CHANGE CHANGE CHANGE CHANGE CHANGE username
            user="fced_sonia_ferreira",  # your username #############CHANGE CHANGE CHANGE CHANGE CHANGE username
            password="Obrigado25.",  # your password #############CHANGE CHANGE CHANGE CHANGE CHANGE password
            host="dbm.fe.up.pt",  # the database host
            port="5433",
            options='-c search_path=races_test') # use the schema you want to connect to #############CHANGE CHANGE CHANGE CHANGE CHANGE to public 
        connected = True

    except psycopg2.OperationalError:
        print("You're not connected to FEUP VPN or inputed wrong credentials.")
    else:
        print("You successfully connected to the database.")
    finally:
        continue


class DisplayRaces:


    """
    Display DB Functions
    """
    def __init__(self):
        self.win = tk.Tk()
        # set initial window size (width, height)
        self.win.minsize(900, 600)
        self.win.attributes("-topmost", True)
        self.win.title("Races Events - Management Studio")
        # call tabs into layout
        self.tab_controls()

    def tab_controls(self):
        """
        START CONTROL TABS
        Tabs are created and the content is nested in a 'LabelFrame'
        Create Tab Content
        """
        
        # ----- Create Record tab control and creation ----
        tab_control = ttk.Notebook(self.win)  # control for tab
        create_tab = ttk.Frame(tab_control)  # create tab

        #-----------------------------------------------------------------------------------------------------------------#
        #-------------------------------------------- READ TAB Runners ---------------------------------------------------#
        read_tab = ttk.Frame(tab_control)  # create tab
        tab_control.add(read_tab, text="Read Runners Record(s)")  # add the tab / nest read record tab
        rtab_frame = ttk.LabelFrame(read_tab,  text=" View Runners ")
        rtab_frame.grid(row=0, column=0, padx=5, pady=5)
     
        def view_runners():
            rlistbox = Listbox(rtab_frame, width=75)
            view_rows = ''

            runner_id = r_rid.get()
            runner_name = r_rname.get()
            if len(runner_name) != 0:
                runner_name = "'%" + runner_name + "%'"

            cur = con.cursor()
            with con:
                if len(runner_id)!= 0 and len(runner_name) == 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_id = {runner_id} ORDER by runner_id LIMIT 1000')
                elif len(runner_id)== 0 and len(runner_name) != 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_name LIKE {runner_name} ORDER by runner_id LIMIT 1000')
                elif len(runner_id)!= 0 and len(runner_name) != 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_id = {runner_id} AND runner_name LIKE {runner_name} ORDER by runner_id LIMIT 1000')
                else:
                    cur.execute(f'SELECT * FROM runner ORDER by runner_id LIMIT 1000 OFFSET 100')
                result = cur.fetchall(); #all
                con.commit()
            for row in result: 
                rlistbox.insert(END, '#' + str(row[0]) + ',  '
                               + str(row[1]) + ',  '
                               + str(row[2]) + ',  '
                               + str(row[3]) + ',  '
                               + str(row[4]) + '\n')

            view_label = ttk.Label(rtab_frame, text="(Scrollable list!)")
            view_label.grid(row=6, padx=5, pady=2, sticky='SE')

            scrollbar = Scrollbar(rtab_frame)
            rlistbox.grid(row=5, sticky='WE')
            rlistbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=rlistbox.yview)

        tk.Label(rtab_frame, text="Runner ID:  ").grid(row=1, sticky=W, padx=5, pady=2)
        r_rid = tk.Entry(rtab_frame, width=25)
        r_rid.grid(row=1)

        tk.Label(rtab_frame, text="Runner Name:  ").grid(row=2, sticky=W, padx=5, pady=2)
        r_rname = tk.Entry(rtab_frame, width=25 )
        r_rname.grid(row=2)

        ttk.Label(rtab_frame, 
                  text="A limit of 1000 records is applied by search, please use selection criteria!").grid(row=4, sticky='WE',column=0)

        view_runners_btn = tk.Button(rtab_frame, text='View Runners', width=45)
        view_runners_btn['command'] = lambda: view_runners()
        view_runners_btn.grid(row=7, sticky='WE', padx=5)
        # ---- End read tab

        #-------------------------------------------------------------------------------------------------------------------#
        #-------------------------------------------- CREATE TAB Runners ---------------------------------------------------#
        tab_control.add(create_tab, text="Create Runners Record(s)")  # add the tab
        ctab_frame = ttk.LabelFrame(create_tab, text=" Add New Runner: \n(Runner ID will be generated automatically!) ")
        ctab_frame.grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(ctab_frame, text=" ").grid(row=1, sticky="W", column=0)

        tk.Label(ctab_frame, text="Name:  ").grid(row=2, sticky=W, padx=5, pady=2)
        rname = tk.Entry(ctab_frame, width=25)
        rname.grid(row=2)

        tk.Label(ctab_frame, text="Sex:  ").grid(row=3, sticky=W, padx=5, pady=2)
        rsex = tk.Entry(ctab_frame, width=25)
        rsex.grid(row=3)

        tk.Label(ctab_frame, text="Nation:  ").grid(row=4, sticky=W, padx=5, pady=2)
        rnation = tk.Entry(ctab_frame, width=25)
        rnation.grid(row=4)

        tk.Label(ctab_frame, text="Birthdate:  ").grid(row=5, sticky=W, padx=5, pady=2)
        rbirthdate = tk.Entry(ctab_frame, width=25)
        rbirthdate.grid(row=5)

        self.new_runner_record_btn = tk.Button(ctab_frame, text='Add Runner', width=45)

        def clear_fields():
            """clear  fields after adding a runner"""
            rname.delete(0, tk.END)
            rsex.delete(0, tk.END)
            rnation.delete(0, tk.END)
            rbirthdate.delete(0, tk.END)
            delete_field.delete(0, tk.END)
            u_rid.delete(0, tk.END)
            u_rname.delete(0, tk.END)
            u_rsex.delete(0, tk.END)
            u_rnation.delete(0, tk.END)
            u_rbirthdate.delete(0, tk.END)

        def new_runner_record(rname, rsex, rnation, rbirthdate):
            """
            wrap the execution so it can be passed to the method
            """
            runner_name = rname.get()
            runner_sex = rsex.get().upper()
            runner_nation = rnation.get().upper()
            runner_birthdate = rbirthdate.get()
            print (runner_name, runner_sex, runner_nation, runner_birthdate)

            # validations!!
            if len(runner_nation) != 2: nt_error = 1 
            else:nt_error = 0
            if runner_sex == 'M' or runner_sex == 'F' : sx_error = 0
            else:sx_error = 1
            dt_error = ""
            try: 
                datetime.datetime.strptime(runner_birthdate, '%Y-%m-%d')
                dt_error == 0
            except ValueError:
                dt_error = 1

            if nt_error == 1 or sx_error == 1 or dt_error == 1: stop = 1
            else: stop = 0

            if stop != 1:
                cur = con.cursor()
                with con:
                    cur.execute(f'SELECT runner_id FROM runner ORDER by runner_id DESC LIMIT 1')
                    result = cur.fetchone()
                    new_rid = result[0] + 1
                    cur.execute(f"INSERT INTO runner VALUES ('{new_rid}', '{runner_name}', '{runner_sex}', '{runner_nation}', '{runner_birthdate}') ")
                    messagebox.showinfo(title="info", message="record ID: " + str(new_rid) + ", " + runner_name + ", " + runner_sex + ", " + runner_nation +
                                        ", " + runner_birthdate + ", successfully inserted!", parent=self.win)
                    con.commit()
                clear_fields() #clean the fields
            else:
                if nt_error == 1 and sx_error == 0 and dt_error == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation", icon='error', parent=self.win )
                elif nt_error == 0 and sx_error == 1 and dt_error == 0 :
                    messagebox.showinfo("info", "Please validate the following field(s): Sex", icon='error', parent=self.win )
                elif nt_error == 0 and sx_error == 0 and dt_error == 1 :
                    messagebox.showinfo("info", "Please validate the following field(s): Date (yyyy-mm-dd)", icon='error', parent=self.win )
                elif sx_error == 1 and nt_error == 1 and dt_error == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Sex", icon='error', parent=self.win )
                elif sx_error == 0 and nt_error == 1 and dt_error == 1:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Date", icon='error', parent=self.win )
                elif sx_error == 1 and nt_error == 0 and dt_error == 1:
                    messagebox.showinfo("info", "Please validate the following field(s): Sex & Date", icon='error', parent=self.win  )
                elif sx_error == 1 and nt_error == 1 and dt_error == 1:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Sex & Date", icon='error', parent=self.win )


        self.new_runner_record_btn['command'] = lambda: new_runner_record(rname, rsex, rnation, rbirthdate)
        self.new_runner_record_btn.grid(row=6, sticky=W, padx=5, pady=5)
        # ---- End create tab
    
        #-----------------------------------------------------------------------------------------------------------------#
        #-------------------------------------------- UPDATE TAB Runners -------------------------------------------------#
        update_tab = ttk.Frame(tab_control)  # create tab
        tab_control.add(update_tab, text="Update Runner Record(s)")  # add the tab

        utab_frame = ttk.LabelFrame(update_tab, text=" Update Runners")
        utab_frame.grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(utab_frame, text="Search the Runner(s) record!").grid(row=1, sticky="WE", column=0)

        def view_update_runners():
            ulistbox = Listbox(utab_frame, width=75)
            view_rows = ''

            u_rid3 = u_rid2.get()
            u_rname3 = u_rname2.get()
            if len(u_rname3) != 0:
                u_rname3 = "'%" + u_rname3 + "%'"

            cur = con.cursor()
            with con:
                if len(u_rid3)!= 0 and len(u_rname3) == 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_id = {u_rid3} ORDER by runner_id LIMIT 1000')
                elif len(u_rid3)== 0 and len(u_rname3) != 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_name LIKE {u_rname3} ORDER by runner_id LIMIT 1000')
                elif len(u_rid3)!= 0 and len(u_rname3) != 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_id = {u_rid3} AND runner_name LIKE {u_rname3} ORDER by runner_id LIMIT 1000')
                else:
                    cur.execute(f'SELECT * FROM runner ORDER by runner_id ')
                result = cur.fetchall(); #all
                con.commit()


                for row in result: 
                    ulistbox.insert(END, '#' + str(row[0]) + ',  '
                                + str(row[1]) + ',  '
                                + str(row[2]) + ',  '
                                + str(row[3]) + ',  '
                                + str(row[4]) + '\n')
                    

            scrollbar = Scrollbar(utab_frame)

            ulistbox.grid(row=5, sticky='WE')
            ulistbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=ulistbox.yview)

        tk.Label(utab_frame, text="Runner ID:  ").grid(row=2, sticky=W, padx=5, pady=2)
        u_rid2 = tk.Entry(utab_frame, width=25)
        u_rid2.grid(row=2)

        tk.Label(utab_frame, text="Runner Name:  ").grid(row=3, sticky=W, padx=5, pady=2)
        u_rname2 = tk.Entry(utab_frame, width=25 )
        u_rname2.grid(row=3)

        ttk.Label(utab_frame, 
        text="A limit of 1000 records is applied by search, please use selection criteria!").grid(row=4, sticky='WE',column=0)

        view_runners_btn = tk.Button(utab_frame, text='View Runners', width=45)
        view_runners_btn['command'] = lambda: view_update_runners()
        view_runners_btn.grid(row=6, sticky='WE', padx=5)

        def update_record():
            u_rid2 = u_rid.get()
            u_rname2 = u_rname.get()
            u_rsex2 = u_rsex.get()
            u_rnation2 = u_rnation.get()
            u_rbirthdate2 = u_rbirthdate.get()
            
            # validations!!
            if len(u_rname2) == 0: nm_error2 = 1 
            else:nm_error2 = 0
            if len(u_rnation2) != 2: nt_error2 = 1 
            else:nt_error2 = 0
            if u_rsex2 == 'M' or u_rsex2 == 'F' : sx_error2 = 0
            else:sx_error2 = 1
            dt_error2 = ""
            try: 
                datetime.datetime.strptime(u_rbirthdate2, '%Y-%m-%d')
                dt_error2 == 0
            except ValueError:
                dt_error2 = 1

            if nt_error2 == 1 or sx_error2 == 1 or dt_error2 == 1: stop2 = 1
            else: stop2 = 0

            if stop2 != 1:
                cur = con.cursor()
                with con:
                    cur.execute(f'SELECT * FROM runner WHERE runner_id = {u_rid2}')
                    result = cur.fetchone()
                    con.commit()
                if result == None:
                    messagebox.showinfo("info", message="Record ID: " + str(d_rid3) + " , doesn't exist! \nChoose a valid ID.", icon='error', parent=self.win )
                else:
                    cur = con.cursor()
                    with con:
                        cur.execute(f"UPDATE runner SET runner_name = '{u_rname2}', sex= '{u_rsex2}', nation = '{u_rnation2}', birthdate = '{u_rbirthdate2}' WHERE runner_id = {u_rid2}")
                        messagebox.showinfo(title="info", message="record ID: " + str(u_rid2) + ", successfully updated!", parent=self.win)
                        con.commit()
                    clear_fields() #clean the fields
                    view_update_runners()
            else:
                if nt_error2 == 1 and sx_error2 == 0  and dt_error2 == 0 and nm_error2 == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation", icon='error', parent=self.win )
                elif nt_error2 == 0 and sx_error2 == 0 and dt_error2 == 0 and nm_error2 == 1:
                    messagebox.showinfo("info", "Please validate the following field(s): Name", icon='error', parent=self.win )
                elif nt_error2 == 0 and sx_error2 == 1 and dt_error2 == 0 and nm_error2 == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Sex", icon='error', parent=self.win )
                elif nt_error2 == 0 and sx_error2 == 0 and dt_error2 == 1 and nm_error2 == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Date (yyyy-mm-dd)", icon='error', parent=self.win )
                elif sx_error2 == 1 and nt_error2 == 1 and dt_error2 == 0 and nm_error2 == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Sex", icon='error', parent=self.win )
                elif sx_error2 == 0 and nt_error2 == 1 and dt_error2 == 1 and nm_error2 == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Date", icon='error', parent=self.win )
                elif sx_error2 == 1 and nt_error2 == 0 and dt_error2 == 1 and nm_error2 == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Sex & Date", icon='error', parent=self.win  )
                elif sx_error2 == 1 and nt_error2 == 1 and dt_error2 == 1 and nm_error2 == 0:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Sex & Date", icon='error', parent=self.win )
                elif sx_error2 == 1 and nt_error2 == 1 and dt_error2 == 0 and nm_error2 == 1:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Sex & Name", icon='error', parent=self.win )
                elif sx_error2 == 1 and nt_error2 == 1 and dt_error2 == 1 and nm_error2 == 1:
                    messagebox.showinfo("info", "Please validate the following field(s): Nation & Sex & Date & Name", icon='error', parent=self.win )



        tk.Label(utab_frame, text="Name:  ").grid(row=8, sticky=W,  padx=5, pady=2)
        u_rname = tk.Entry(utab_frame, width=20)
        u_rname.grid(row=8)

        tk.Label(utab_frame, text="Sex:  ").grid(row=9, sticky=W, padx=5, pady=2)
        u_rsex = tk.Entry(utab_frame, width=20)
        u_rsex.grid(row=9)

        tk.Label(utab_frame, text="Nation:  ").grid(row=10, sticky=W, padx=5, pady=2)
        u_rnation = tk.Entry(utab_frame, width=20)
        u_rnation.grid(row=10)

        tk.Label(utab_frame, text="Birth Date:  ").grid(row=11, sticky=W, padx=5, pady=2)
        u_rbirthdate = tk.Entry(utab_frame, width=20)
        u_rbirthdate.grid(row=11)

        update_label = Label(utab_frame, text='Runner id: ')
        update_label.grid(row=12, sticky='W', padx=5, pady=5)
        u_rid = Entry(utab_frame, width=15)
        u_rid.grid(row=12, padx=5, pady=5)
        update_runner_btn = tk.Button(utab_frame, text='Update Record', width=15)

        update_runner_btn['command'] = lambda: update_record()
        update_runner_btn.grid(row=13, sticky='E', padx=5, pady=5)
        # ---- End UPDATE TAB

        # ---------------------------------------------------------------------------------------------------
        # -------------------------------------- Start DELETE TAB Content -----------------------------------
        delete_tab = ttk.Frame(tab_control)
        tab_control.add(delete_tab, text="Delete Runner Record")

        dtab_frame = ttk.LabelFrame(delete_tab, text=" Delete Runner: ")
        dtab_frame.grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(dtab_frame, text="Search the Runner(s) record!").grid(row=0, sticky="W", column=0)

        def view_delete_runners():
            dlistbox = Listbox(dtab_frame, width=75)
            view_rows = ''

            d_rid2 = d_rid.get()
            d_rname2 = d_rname.get()
            if len(d_rname2) != 0:
                d_rname2 = "'%" + d_rname2 + "%'"

            cur = con.cursor()
            with con:
                if len(d_rid2)!= 0 and len(d_rname2) == 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_id = {d_rid2} ORDER by runner_id LIMIT 1000')
                elif len(d_rid2)== 0 and len(d_rname2) != 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_name LIKE {d_rname2} ORDER by runner_id LIMIT 1000')
                elif len(d_rid2)!= 0 and len(d_rname2) != 0:
                    cur.execute(f'SELECT * FROM runner WHERE runner_id = {d_rid2} AND runner_name LIKE {d_rname2} ORDER by runner_id LIMIT 1000')
                else:
                    cur.execute(f'SELECT * FROM runner ORDER by runner_id ')
                con.commit()
                result = cur.fetchall(); #all

            for row in result: 
                dlistbox.insert(END, '#' + str(row[0]) + ',  '
                               + str(row[1]) + ',  '
                               + str(row[2]) + ',  '
                               + str(row[3]) + ',  '
                               + str(row[4]) + '\n')

                view_label = ttk.Label(dtab_frame, text="(Scrollable list!)")
                view_label.grid(row=6, padx=5, pady=2, sticky='SE')

                scrollbar = Scrollbar(dtab_frame)
                dlistbox.grid(row=5, sticky='WE')
                dlistbox.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=dlistbox.yview)

        tk.Label(dtab_frame, text="Runner ID:  ").grid(row=2, sticky=W, padx=5, pady=2)
        d_rid = tk.Entry(dtab_frame, width=25)
        d_rid.grid(row=2)

        tk.Label(dtab_frame, text="Runner Name:  ").grid(row=3, sticky=W, padx=5, pady=2)
        d_rname = tk.Entry(dtab_frame, width=25 )
        d_rname.grid(row=3)

        ttk.Label(dtab_frame, 
                  text="A limit of 1000 records is applied by search, please use selection criteria!").grid(row=4, sticky='WE',column=0)

        
        view_runners_btn = tk.Button(dtab_frame, text='View Runners', width=45)
        view_runners_btn['command'] = lambda: view_delete_runners()
        view_runners_btn.grid(row=7, sticky='WE', padx=5)
        

        def delete_record():
            d_rid3 = delete_field.get()

            cur = con.cursor()
            with con:
                cur.execute(f'SELECT * FROM runner WHERE runner_id = {d_rid3}')
                result = cur.fetchone()
                con.commit()
            if result == None:
                messagebox.showinfo("info", message="Record ID: " + str(d_rid3) + " , doesn't exist! \nChoose a valid ID.", icon='error', parent=self.win )
            else:
                cur = con.cursor()
                with con:
                    cur.execute(f"DELETE FROM runner WHERE runner_id = {d_rid3}")
                    messagebox.showinfo(title="info", message="record ID: " + str(d_rid3) + ", successfully deleted!", parent=self.win)
                    con.commit()

            clear_fields() 
            view_delete_runners()

        tk.Label(dtab_frame, text="Insert Runner ID for DEL:  ").grid(row=9, sticky=W, padx=5, pady=2)
        delete_field = Entry(dtab_frame, width=10)
        delete_field.grid(row=9, padx=5, pady=5)
        delete_runner_btn = tk.Button(dtab_frame, text='Delete Record', width=15)
        delete_runner_btn['command'] = lambda: delete_record()
        delete_runner_btn.grid(row=9, sticky='E', padx=5, pady=5)
        # ---- End DELETE TAB



        # ---------------------------------------------------------------------------------------------------
        # -------------------------------------- TABS FUNCS -----------------------------------
        tab_control.grid()  # to make tabs visible


        # ---------------------------------------------------------------------------------------------------
        # -------------------------------------- MENU BAR ACTIONS -----------------------------------
        def _quit():  # priv func
            # Quit/Destroy Application GUI cleanly
            con.commit()
            con.close()
            self.win.quit()
            self.win.destroy()
            exit()

        # Top Menu bar
        menu_bar = Menu(self.win)
        self.win.config(menu=menu_bar)
        # File Menu Bar items
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=_quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # help/about menu bar items
        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="Runners Data Management Application, "
                                     "Ⓒ 2022Edition MECD - Databases - GROUP9??")   # ----- ????????CHECK THE GROUP NR
        menu_bar.add_cascade(label="About", menu=about_menu)

        self.win.mainloop()

if __name__ == '__main__':
    DisplayRaces()
