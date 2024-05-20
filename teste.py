import tkinter as tk
from tkinter import messagebox

def delete_selected(event=None):
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("Warning", "No item selected")

root = tk.Tk()
root.title("Keyboard Delete Example")

listbox = tk.Listbox(root)
listbox.pack(pady=20)

# Add some sample items to the listbox
for item in ["Item 1", "Item 2", "Item 3", "Item 4"]:
    listbox.insert(tk.END, item)

delete_button = tk.Button(root, text="Delete", command=delete_selected)
delete_button.pack(pady=20)

# Bind the 'Delete' key to the delete_selected function
root.bind('<Delete>', delete_selected)

root.mainloop()
