# ============================================================
#              DEBANSHU'S SCIENTIFIC CALCULATOR
#              Developed By: Debanshu Guchhait
# ============================================================

import tkinter as tk
import ast
import operator
import json
import os
import math


# ============================================================
# WINDOW SETUP
# ============================================================

root = tk.Tk()

root.title("Debanshu's Calculator")
root.geometry("430x700")
root.resizable(False, False)
root.configure(bg="#080c14")


# ============================================================
# COLOR PALETTE
# ============================================================

BG = "#080c14"

CARD = "#111827"
CARD_LIGHT = "#172033"

DISPLAY_BG = "#0d1422"

TEXT = "#f8fafc"
SECONDARY = "#94a3b8"

NUMBER = "#1b2638"
NUMBER_HOVER = "#26364d"

OPERATOR = "#25235c"
OPERATOR_HOVER = "#34318a"

SPECIAL = "#344154"
SPECIAL_HOVER = "#46556b"

CLEAR = "#b91c1c"
CLEAR_HOVER = "#dc2626"

BACKSPACE = "#b45309"
BACKSPACE_HOVER = "#d97706"

EQUAL = "#059669"
EQUAL_HOVER = "#10b981"

HISTORY = "#18243a"
HISTORY_HOVER = "#263a5c"

ACCENT = "#60a5fa"


# ============================================================
# HISTORY FILE
# ============================================================

HISTORY_FILE = "calculator_history.json"


# ============================================================
# ANGLE MODE
# ============================================================

angle_mode = "DEG"


# ============================================================
# HISTORY
# ============================================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception:

        return []


history = load_history()


def save_history():

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=4
            )

    except Exception as error:

        print(
            "History save error:",
            error
        )


# ============================================================
# MAIN CONTAINER
# ============================================================

main_frame = tk.Frame(
    root,
    bg=BG
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=16,
    pady=14
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    main_frame,
    bg=BG
)

header.pack(
    fill="x",
    pady=(0, 12)
)


# ============================================================
# TITLE
# ============================================================

title_frame = tk.Frame(
    header,
    bg=BG
)

title_frame.pack(
    side="left"
)


title = tk.Label(
    title_frame,
    text="CALCULATOR",
    font=("Segoe UI", 21, "bold"),
    bg=BG,
    fg=ACCENT
)

title.pack(
    anchor="w"
)


subtitle = tk.Label(
    title_frame,
    text="SIMPLE • FAST • SMART",
    font=("Segoe UI", 7, "bold"),
    bg=BG,
    fg=SECONDARY
)

subtitle.pack(
    anchor="w",
    pady=(1, 0)
)


# ============================================================
# SCIENTIFIC TOGGLE
# ============================================================

scientific_visible = False


def toggle_scientific():

    global scientific_visible

    if scientific_visible:

        scientific_frame.pack_forget()

        scientific_visible = False

        scientific_button.config(
            text="SCI",
            bg=SPECIAL
        )

    else:

        scientific_frame.pack(
            fill="x",
            pady=(0, 8),
            before=buttons_frame
        )

        scientific_visible = True

        scientific_button.config(
            text="BASIC",
            bg=OPERATOR
        )


scientific_button = tk.Button(
    header,
    text="SCI",
    command=toggle_scientific,
    font=("Segoe UI", 9, "bold"),
    bg=SPECIAL,
    fg=TEXT,
    activebackground=SPECIAL_HOVER,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=9,
    pady=5
)

scientific_button.pack(
    side="right",
    padx=(0, 6),
    pady=5
)


# ============================================================
# HISTORY TOGGLE
# ============================================================

history_visible = False


def toggle_history():

    global history_visible

    if history_visible:

        history_card.pack_forget()

        history_visible = False

        history_button.config(
            text="🕘",
            bg=HISTORY
        )

    else:

        history_card.pack(
            fill="x",
            pady=(0, 12),
            before=display_card
        )

        history_visible = True

        history_button.config(
            text="✕",
            bg=HISTORY_HOVER
        )


history_button = tk.Button(
    header,
    text="🕘",
    command=toggle_history,
    font=("Segoe UI", 12, "bold"),
    bg=HISTORY,
    fg=TEXT,
    activebackground=HISTORY_HOVER,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    width=3,
    height=1
)

history_button.pack(
    side="right",
    pady=5
)


# ============================================================
# HISTORY CARD
# ============================================================

history_card = tk.Frame(
    main_frame,
    bg=CARD,
    highlightthickness=1,
    highlightbackground="#1e293b"
)


# ============================================================
# HISTORY HEADER
# ============================================================

history_top = tk.Frame(
    history_card,
    bg=CARD
)

history_top.pack(
    fill="x"
)


history_title = tk.Label(
    history_top,
    text="◷  HISTORY",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=ACCENT
)

history_title.pack(
    side="left",
    padx=12,
    pady=8
)


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_history():

    history.clear()

    save_history()

    refresh_history()


clear_history_button = tk.Button(
    history_top,
    text="CLEAR",
    command=clear_history,
    font=("Segoe UI", 8, "bold"),
    bg="#374151",
    fg=TEXT,
    activebackground=CLEAR_HOVER,
    activeforeground=TEXT,
    relief="flat",
    bd=0,
    cursor="hand2",
    padx=10,
    pady=3
)

clear_history_button.pack(
    side="right",
    padx=8,
    pady=5
)


# ============================================================
# HISTORY LIST
# ============================================================

history_area = tk.Frame(
    history_card,
    bg=CARD
)

history_area.pack(
    fill="x",
    padx=7,
    pady=(0, 7)
)


history_scrollbar = tk.Scrollbar(
    history_area
)

history_scrollbar.pack(
    side="right",
    fill="y"
)


history_list = tk.Listbox(
    history_area,
    height=4,
    bg=CARD_LIGHT,
    fg=TEXT,
    font=("Segoe UI", 10),
    selectbackground="#2563eb",
    selectforeground="white",
    relief="flat",
    bd=0,
    highlightthickness=0,
    activestyle="none",
    yscrollcommand=history_scrollbar.set
)

history_list.pack(
    side="left",
    fill="x",
    expand=True
)


history_scrollbar.config(
    command=history_list.yview
)


# ============================================================
# DISPLAY CARD
# ============================================================

display_card = tk.Frame(
    main_frame,
    bg=DISPLAY_BG,
    highlightthickness=1,
    highlightbackground="#26354c"
)

display_card.pack(
    fill="x",
    pady=(0, 12)
)


# ============================================================
# EXPRESSION LABEL
# ============================================================

history_label = tk.Label(
    display_card,
    text="",
    anchor="e",
    bg=DISPLAY_BG,
    fg=SECONDARY,
    font=("Segoe UI", 10)
)

history_label.pack(
    fill="x",
    padx=16,
    pady=(12, 0)
)


# ============================================================
# MAIN DISPLAY
# ============================================================

e1 = tk.Entry(
    display_card,
    font=("Segoe UI", 30, "bold"),
    bg=DISPLAY_BG,
    fg=TEXT,
    insertbackground=ACCENT,
    justify="right",
    relief="flat",
    bd=0
)

e1.pack(
    fill="x",
    padx=16,
    pady=(3, 13),
    ipady=5
)


# ============================================================
# OPERATORS
# ============================================================

operators = {

    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos

}


# ============================================================
# SCIENTIFIC FUNCTIONS
# ============================================================

scientific_functions = {

    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil

}


# ============================================================
# SAFE EVALUATION
# ============================================================

def safe_eval(expression):

    expression = expression.replace(
        "×",
        "*"
    )

    expression = expression.replace(
        "x",
        "*"
    )

    expression = expression.replace(
        "÷",
        "/"
    )

    expression = expression.replace(
        "^",
        "**"
    )

    expression = expression.replace(
        "π",
        "pi"
    )

    # --------------------------------------------------------
    # AST EVALUATION
    # --------------------------------------------------------

    def evaluate(node):

        # ----------------------------------------------------
        # NUMBERS
        # ----------------------------------------------------

        if isinstance(
            node,
            ast.Constant
        ):

            if isinstance(
                node.value,
                (int, float)
            ):

                return node.value

            raise ValueError(
                "Invalid number"
            )

        # ----------------------------------------------------
        # CONSTANTS
        # ----------------------------------------------------

        if isinstance(
            node,
            ast.Name
        ):

            if node.id == "pi":

                return math.pi

            if node.id == "e":

                return math.e

            raise ValueError(
                "Unknown constant"
            )

        # ----------------------------------------------------
        # BINARY OPERATIONS
        # ----------------------------------------------------

        if isinstance(
            node,
            ast.BinOp
        ):

            left = evaluate(
                node.left
            )

            right = evaluate(
                node.right
            )

            operation = operators.get(
                type(node.op)
            )

            if operation is None:

                raise ValueError(
                    "Invalid operator"
                )

            return operation(
                left,
                right
            )

        # ----------------------------------------------------
        # UNARY OPERATIONS
        # ----------------------------------------------------

        if isinstance(
            node,
            ast.UnaryOp
        ):

            value = evaluate(
                node.operand
            )

            operation = operators.get(
                type(node.op)
            )

            if operation is None:

                raise ValueError(
                    "Invalid operator"
                )

            return operation(
                value
            )

        # ----------------------------------------------------
        # FUNCTION CALL
        # ----------------------------------------------------

        if isinstance(
            node,
            ast.Call
        ):

            if not isinstance(
                node.func,
                ast.Name
            ):

                raise ValueError(
                    "Invalid function"
                )

            function_name = node.func.id

            if len(node.args) != 1:

                raise ValueError(
                    "Function requires one argument"
                )

            value = evaluate(
                node.args[0]
            )

            # ------------------------------------------------
            # SQRT / LOG / LN
            # ------------------------------------------------

            if function_name in scientific_functions:

                return scientific_functions[
                    function_name
                ](value)

            # ------------------------------------------------
            # SIN
            # ------------------------------------------------

            if function_name == "sin":

                if angle_mode == "DEG":

                    value = math.radians(
                        value
                    )

                return math.sin(value)

            # ------------------------------------------------
            # COS
            # ------------------------------------------------

            if function_name == "cos":

                if angle_mode == "DEG":

                    value = math.radians(
                        value
                    )

                return math.cos(value)

            # ------------------------------------------------
            # TAN
            # ------------------------------------------------

            if function_name == "tan":

                if angle_mode == "DEG":

                    value = math.radians(
                        value
                    )

                return math.tan(value)

            raise ValueError(
                "Unknown function"
            )

        raise ValueError(
            "Invalid expression"
        )

    tree = ast.parse(
        expression,
        mode="eval"
    )

    return evaluate(
        tree.body
    )


# ============================================================
# FORMAT RESULT
# ============================================================

def format_result(result):

    if isinstance(
        result,
        float
    ):

        if math.isinf(result):

            return "Infinity"

        if math.isnan(result):

            return "Error"

        if result.is_integer():

            return str(
                int(result)
            )

        return f"{result:.12g}"

    return str(result)


# ============================================================
# CLICK
# ============================================================

def click(value):

    current = e1.get()

    if current in (
        "Error",
        "Infinity"
    ):

        current = ""

    e1.delete(
        0,
        tk.END
    )

    e1.insert(
        0,
        current + str(value)
    )


# ============================================================
# CLEAR
# ============================================================

def clear():

    e1.delete(
        0,
        tk.END
    )

    history_label.config(
        text=""
    )


# ============================================================
# BACKSPACE
# ============================================================

def backspace():

    current = e1.get()

    e1.delete(
        0,
        tk.END
    )

    e1.insert(
        0,
        current[:-1]
    )


# ============================================================
# EQUAL
# ============================================================

def equal():

    expression = e1.get().strip()

    if not expression:

        return

    try:

        result = safe_eval(
            expression
        )

        result = format_result(
            result
        )

        history_label.config(
            text=expression
        )

        e1.delete(
            0,
            tk.END
        )

        e1.insert(
            0,
            result
        )

        history.insert(
            0,
            {
                "expression": expression,
                "result": result
            }
        )

        if len(history) > 100:

            del history[100:]

        save_history()

        refresh_history()

        history_list.yview_moveto(
            0
        )

    except ZeroDivisionError:

        history_label.config(
            text="Cannot divide by zero"
        )

        e1.delete(
            0,
            tk.END
        )

        e1.insert(
            0,
            "Error"
        )

    except ValueError as error:

        history_label.config(
            text=str(error)
        )

        e1.delete(
            0,
            tk.END
        )

        e1.insert(
            0,
            "Error"
        )

    except Exception:

        history_label.config(
            text="Invalid Expression"
        )

        e1.delete(
            0,
            tk.END
        )

        e1.insert(
            0,
            "Error"
        )


# ============================================================
# SCIENTIFIC FUNCTION
# ============================================================

def scientific_function(name):

    current = e1.get().strip()

    if not current:

        return

    try:

        # ----------------------------------------------------
        # FUNCTION BASED OPERATIONS
        # ----------------------------------------------------

        if name in (
            "sqrt",
            "sin",
            "cos",
            "tan",
            "log",
            "ln"
        ):

            expression = (
                f"{name}({current})"
            )

            result = safe_eval(
                expression
            )

        # ----------------------------------------------------
        # SQUARE
        # ----------------------------------------------------

        elif name == "square":

            expression = (
                f"({current})^2"
            )

            result = safe_eval(
                expression
            )

        # ----------------------------------------------------
        # FACTORIAL
        # ----------------------------------------------------

        elif name == "factorial":

            value = safe_eval(
                current
            )

            if value < 0:

                raise ValueError(
                    "Factorial requires a non-negative number"
                )

            if not float(value).is_integer():

                raise ValueError(
                    "Factorial requires an integer"
                )

            result = math.factorial(
                int(value)
            )

            expression = (
                f"{current}!"
            )

        else:

            raise ValueError(
                "Unknown scientific function"
            )

        result = format_result(
            result
        )

        history_label.config(
            text=expression
        )

        e1.delete(
            0,
            tk.END
        )

        e1.insert(
            0,
            result
        )

        history.insert(
            0,
            {
                "expression": expression,
                "result": result
            }
        )

        if len(history) > 100:

            del history[100:]

        save_history()

        refresh_history()

        history_list.yview_moveto(
            0
        )

    except ValueError as error:

        history_label.config(
            text=str(error)
        )

        e1.delete(
            0,
            tk.END
        )

        e1.insert(
            0,
            "Error"
        )

    except Exception:

        history_label.config(
            text="Invalid Scientific Expression"
        )

        e1.delete(
            0,
            tk.END
        )

        e1.insert(
            0,
            "Error"
        )


# ============================================================
# TOGGLE DEG / RAD
# ============================================================

def toggle_angle_mode():

    global angle_mode

    if angle_mode == "DEG":

        angle_mode = "RAD"

    else:

        angle_mode = "DEG"

    angle_button.config(
        text=angle_mode
    )


# ============================================================
# REFRESH HISTORY
# ============================================================

def refresh_history():

    history_list.delete(
        0,
        tk.END
    )

    if not history:

        history_list.insert(
            tk.END,
            "   No calculation history"
        )

        return

    for item in history:

        expression = item.get(
            "expression",
            ""
        )

        result = item.get(
            "result",
            ""
        )

        history_list.insert(
            tk.END,
            f"   {expression}  =  {result}"
        )


# ============================================================
# USE HISTORY
# ============================================================

def use_history(event):

    selection = history_list.curselection()

    if not selection:

        return

    index = selection[0]

    if index >= len(history):

        return

    item = history[index]

    e1.delete(
        0,
        tk.END
    )

    e1.insert(
        0,
        item["result"]
    )

    history_label.config(
        text=item["expression"]
    )


history_list.bind(
    "<Double-Button-1>",
    use_history
)


# ============================================================
# KEYBOARD SUPPORT
# ============================================================

def keyboard_input(event):

    key = event.keysym

    if event.char in "0123456789+-*/().%":

        click(
            event.char
        )

    elif event.char == "^":

        click("^")

    elif event.char.lower() == "x":

        click("x")

    elif key in (
        "Return",
        "KP_Enter"
    ):

        equal()

    elif key == "BackSpace":

        backspace()

    elif key == "Escape":

        clear()


root.bind(
    "<Key>",
    keyboard_input
)


# ============================================================
# SCIENTIFIC FUNCTIONS FRAME
# ============================================================

scientific_frame = tk.Frame(
    main_frame,
    bg=BG
)


def create_scientific_button(
    text,
    command,
    row,
    column,
    bg=OPERATOR,
    hover=OPERATOR_HOVER
):

    button = tk.Button(
        scientific_frame,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=bg,
        fg=TEXT,
        activebackground=hover,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    button.grid(
        row=row,
        column=column,
        padx=3,
        pady=3,
        sticky="nsew"
    )

    def on_enter(event):

        button.config(
            bg=hover
        )

    def on_leave(event):

        button.config(
            bg=bg
        )

    button.bind(
        "<Enter>",
        on_enter
    )

    button.bind(
        "<Leave>",
        on_leave
    )

    return button


for column in range(5):

    scientific_frame.columnconfigure(
        column,
        weight=1
    )


# ============================================================
# SCIENTIFIC ROW 1
# ============================================================

angle_button = create_scientific_button(
    "DEG",
    toggle_angle_mode,
    0,
    0,
    bg=SPECIAL,
    hover=SPECIAL_HOVER
)


create_scientific_button(
    "√",
    lambda: scientific_function("sqrt"),
    0,
    1
)


create_scientific_button(
    "x²",
    lambda: scientific_function("square"),
    0,
    2
)


create_scientific_button(
    "log",
    lambda: scientific_function("log"),
    0,
    3
)


create_scientific_button(
    "ln",
    lambda: scientific_function("ln"),
    0,
    4
)


# ============================================================
# SCIENTIFIC ROW 2
# ============================================================

create_scientific_button(
    "sin",
    lambda: scientific_function("sin"),
    1,
    0
)


create_scientific_button(
    "cos",
    lambda: scientific_function("cos"),
    1,
    1
)


create_scientific_button(
    "tan",
    lambda: scientific_function("tan"),
    1,
    2
)


create_scientific_button(
    "π",
    lambda: click("π"),
    1,
    3,
    bg=SPECIAL,
    hover=SPECIAL_HOVER
)


create_scientific_button(
    "e",
    lambda: click("e"),
    1,
    4,
    bg=SPECIAL,
    hover=SPECIAL_HOVER
)


# ============================================================
# SCIENTIFIC ROW 3
# ============================================================

create_scientific_button(
    "!",
    lambda: scientific_function("factorial"),
    2,
    0
)


create_scientific_button(
    "xʸ",
    lambda: click("^"),
    2,
    1
)


# ============================================================
# BASIC BUTTON FRAME
# ============================================================

buttons_frame = tk.Frame(
    main_frame,
    bg=BG
)

buttons_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# BASIC BUTTON HELPER
# ============================================================

def create_button(
    text,
    command,
    row,
    column,
    bg=NUMBER,
    hover=NUMBER_HOVER,
    colspan=1,
    rowspan=1
):

    button = tk.Button(
        buttons_frame,
        text=text,
        command=command,
        font=("Segoe UI", 14, "bold"),
        bg=bg,
        fg=TEXT,
        activebackground=hover,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    button.grid(
        row=row,
        column=column,
        columnspan=colspan,
        rowspan=rowspan,
        padx=4,
        pady=4,
        sticky="nsew"
    )

    def on_enter(event):

        button.config(
            bg=hover
        )

    def on_leave(event):

        button.config(
            bg=bg
        )

    button.bind(
        "<Enter>",
        on_enter
    )

    button.bind(
        "<Leave>",
        on_leave
    )

    return button


# ============================================================
# BASIC GRID
# ============================================================

for column in range(5):

    buttons_frame.columnconfigure(
        column,
        weight=1
    )


for row in range(5):

    buttons_frame.rowconfigure(
        row,
        weight=1
    )


# ============================================================
# BASIC ROW 1
# ============================================================

create_button(
    "AC",
    clear,
    0,
    0,
    bg=CLEAR,
    hover=CLEAR_HOVER,
    colspan=2
)


create_button(
    "⌫",
    backspace,
    0,
    2,
    bg=BACKSPACE,
    hover=BACKSPACE_HOVER
)


create_button(
    "%",
    lambda: click("%"),
    0,
    3,
    bg=OPERATOR,
    hover=OPERATOR_HOVER
)


create_button(
    "÷",
    lambda: click("/"),
    0,
    4,
    bg=OPERATOR,
    hover=OPERATOR_HOVER
)


# ============================================================
# BASIC ROW 2
# ============================================================

create_button(
    "7",
    lambda: click(7),
    1,
    0
)


create_button(
    "8",
    lambda: click(8),
    1,
    1
)


create_button(
    "9",
    lambda: click(9),
    1,
    2
)


create_button(
    "×",
    lambda: click("x"),
    1,
    3,
    bg=OPERATOR,
    hover=OPERATOR_HOVER
)


create_button(
    "^",
    lambda: click("^"),
    1,
    4,
    bg=OPERATOR,
    hover=OPERATOR_HOVER
)


# ============================================================
# BASIC ROW 3
# ============================================================

create_button(
    "4",
    lambda: click(4),
    2,
    0
)


create_button(
    "5",
    lambda: click(5),
    2,
    1
)


create_button(
    "6",
    lambda: click(6),
    2,
    2
)


create_button(
    "−",
    lambda: click("-"),
    2,
    3,
    bg=OPERATOR,
    hover=OPERATOR_HOVER
)


create_button(
    "(",
    lambda: click("("),
    2,
    4,
    bg=SPECIAL,
    hover=SPECIAL_HOVER
)


# ============================================================
# BASIC ROW 4
# ============================================================

create_button(
    "1",
    lambda: click(1),
    3,
    0
)


create_button(
    "2",
    lambda: click(2),
    3,
    1
)


create_button(
    "3",
    lambda: click(3),
    3,
    2
)


create_button(
    "+",
    lambda: click("+"),
    3,
    3,
    bg=OPERATOR,
    hover=OPERATOR_HOVER
)


create_button(
    ")",
    lambda: click(")"),
    3,
    4,
    bg=SPECIAL,
    hover=SPECIAL_HOVER
)


# ============================================================
# BASIC ROW 5
# ============================================================

create_button(
    "0",
    lambda: click(0),
    4,
    0,
    colspan=2
)


create_button(
    ".",
    lambda: click("."),
    4,
    2
)


create_button(
    "=",
    equal,
    4,
    3,
    bg=EQUAL,
    hover=EQUAL_HOVER,
    colspan=2
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    main_frame,
    text="⚡ Developed by Debanshu Guchhait",
    bg=BG,
    fg="#64748b",
    font=("Segoe UI", 8, "bold")
)

footer.pack(
    pady=(10, 0)
)


# ============================================================
# INITIALIZE
# ============================================================

refresh_history()

e1.focus_set()

root.mainloop()
