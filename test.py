from tkinter import *
  
  
# Creating the root window
root = Tk()
  
# Creating a Listbox and
# attaching it to root window
listbox = Listbox(root)
  
# Adding Listbox to the left
# side of root window
listbox.pack(side = LEFT, fill = BOTH)
  
# Creating a Scrollbar and 
# attaching it to root window
scrollbar = Scrollbar(root)
  
# Adding Scrollbar to the right
# side of root window
scrollbar.pack(side = RIGHT, fill = BOTH)
  
# Insert elements into the listbox
for values in range(100):
    listbox.insert(END, values)
      
# Attaching Listbox to Scrollbar
# Since we need to have a vertical 
# scroll we use yscrollcommand
listbox.config(yscrollcommand = scrollbar.set)
  
# setting scrollbar command parameter 
# to listbox.yview method its yview because
# we need to have a vertical view
scrollbar.config(command = listbox.yview)
  
root.mainloop()