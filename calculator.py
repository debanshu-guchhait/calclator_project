# ==========================================
# Python Tkinter Calculator
# Developed By: Debanshu Guchhait
# ==========================================

from tkinter import *

# =========================
# Window Setup
# =========================

root = Tk()
root.title("Debanshu's Calculator")
root.configure(bg="#1e1e1e")
root.geometry("400x500")
root.resizable(False, False)

# =========================
# Display
# =========================

e1 = Entry(
    root,
    width=21,
    font=('Arial', 20),
    borderwidth=5,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white",
    justify=RIGHT
)

e1.grid(row=0, column=0, columnspan=5, padx=20, pady=10)

# =========================
# Result Label
# =========================

e2 = Label(
    root,
    text="",
    bg="#1e1e1e",
    fg="lightgreen",
    font=("Arial", 10)
)

e2.grid(row=1, column=0, columnspan=5, pady=(0, 10))

# =========================
# Functions
# =========================

# Function to insert numbers/operators

def click(value):
    current = e1.get()
    e1.delete(0, END)
    e1.insert(0, current + str(value))


# Function to clear display

def clear():
    e1.delete(0, END)
    e2.config(text="")


# Function to delete one character

def backspace():
    current = e1.get()
    e1.delete(0, END)
    e1.insert(0, current[:-1])


# Function to calculate result

def equal():
    try:
        expression = e1.get().replace("^", "**").replace("x", "*")

        result = eval(expression)

        e1.delete(0, END)
        e1.insert(0, result)

        e2.config(text=f"Result = {result}")

    except:
        e1.delete(0, END)
        e1.insert(0, "Error")

        e2.config(text="Invalid Expression")

# ===========================================
# Buttons
# ===========================================


# ================= ROW 1 =================

Button(root, width=17, height=3, text="AC",
       command=clear, bg="red").grid(row=2, column=0, columnspan=2, padx=5, pady=5)

Button(root, width=7, height=3, text="^",
       command=lambda: click("^")).grid(row=2, column=2, padx=5, pady=5)

Button(root, width=7, height=3, text="/",
       command=lambda: click("/")).grid(row=2, column=3, padx=5, pady=5)

Button(root, width=7, height=3, text="%",
       command=lambda: click("%")).grid(row=2, column=4, padx=5, pady=5)

# ================= ROW 2 =================

Button(root, width=7, height=3, text="7",
       command=lambda: click(7)).grid(row=3, column=0, padx=5, pady=5)

Button(root, width=7, height=3, text="8",
       command=lambda: click(8)).grid(row=3, column=1, padx=5, pady=5)

Button(root, width=7, height=3, text="9",
       command=lambda: click(9)).grid(row=3, column=2, padx=5, pady=5)

Button(root, width=7, height=3, text="x",
       command=lambda: click("x")).grid(row=3, column=3, padx=5, pady=5)

Button(root, width=7, height=3, text="(",
       command=lambda: click("(")).grid(row=3, column=4, padx=5, pady=5)

# ================= ROW 3 =================

Button(root, width=7, height=3, text="4",
       command=lambda: click(4)).grid(row=4, column=0, padx=5, pady=5)

Button(root, width=7, height=3, text="5",
       command=lambda: click(5)).grid(row=4, column=1, padx=5, pady=5)

Button(root, width=7, height=3, text="6",
       command=lambda: click(6)).grid(row=4, column=2, padx=5, pady=5)

Button(root, width=7, height=3, text="-",
       command=lambda: click("-")).grid(row=4, column=3, padx=5, pady=5)

Button(root, width=7, height=3, text=")",
       command=lambda: click(")")).grid(row=4, column=4, padx=5, pady=5)

# ================= ROW 4 =================

Button(root, width=7, height=3, text="1",
       command=lambda: click(1)).grid(row=5, column=0, padx=5, pady=5)

Button(root, width=7, height=3, text="2",
       command=lambda: click(2)).grid(row=5, column=1, padx=5, pady=5)

Button(root, width=7, height=3, text="3",
       command=lambda: click(3)).grid(row=5, column=2, padx=5, pady=5)

Button(root, width=7, height=3, text="+",
       command=lambda: click("+")).grid(row=5, column=3, padx=5, pady=5)

Button(root, width=7, height=7, text="=",
       command=equal,
       bg="orange").grid(row=5, column=4, rowspan=2, padx=5, pady=5)

# ================= ROW 5 =================

Button(root, width=17, height=3, text="0",
       command=lambda: click(0)).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

Button(root, width=7, height=3, text=".",
       command=lambda: click(".")).grid(row=6, column=2, padx=5, pady=5)

Button(root, width=7, height=3, text="⌫",
       command=backspace,bg="lightcoral").grid(row=6, column=3, padx=5, pady=5)

# =========================
# Footer / Credit / Developer Info
# =========================

Label(
    root,
    text="Developed By Debanshu Guchhait",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=7, column=0, columnspan=5, pady=15)

# =========================
# Run Application
# =========================

root.mainloop()
