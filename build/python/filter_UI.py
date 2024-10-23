import tkinter as tk
from tkinter import messagebox


def on_done():
    global filter_str
    filter_str = text_box.get("1.0", tk.END).strip()  
    global auth_checkbox_state
    global inst_checkbox_state
    auth_checkbox_state = author_var.get()  
    inst_checkbox_state = institution_var.get() 
    root.destroy()

    print(f"Author Checkbox state: {auth_checkbox_state}")
    print(f"Institution Checkbox state: {inst_checkbox_state}")
    print(f"The value of filter_str is: {filter_str}")

def on_checkbox_change(var):
    if var.get():
        if author_var.get() and institution_var.get():
            if var == author_var:
                institution_var.set(False)
            else:
                author_var.set(False)


root = tk.Tk()
root.title("Popup Window")

author_var = tk.BooleanVar()
author_checkbox = tk.Checkbutton(root, text="Author", variable=author_var, command=lambda: on_checkbox_change(author_var))
author_checkbox.pack(pady=10)

institution_var = tk.BooleanVar()
institution_checkbox = tk.Checkbutton(root, text="Institution", variable=institution_var, command=lambda: on_checkbox_change(institution_var))
institution_checkbox.pack(pady=10)

text_box = tk.Text(root, height=5, width=30)
text_box.pack(pady=10)

done_button = tk.Button(root, text="Done", command=on_done)
done_button.pack(pady=10)

root.mainloop()

if auth_checkbox_state is True:
    print("Author")
    filter_str = f'authorships.author.id:{filter_str}'
    print(f"{filter_str}")
else:
    print("Institution")
    filter_str = f'authorships.institutions.lineage:{filter_str}'
    print(f"{filter_str}")

def str_fill():
    filtering = filter_str
    return filtering

