
import tkinter as tk
import ast
import operator

# Calculator window
root = tk.Tk()
root.title("Modern Calculator")
root.geometry("360x540")
root.resizable(False, False)
root.configure(bg="#FACC15")

expression = ""

# Safe mathematical operations
operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg
}

def calculate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in operations:
        left = calculate(node.left)
        right = calculate(node.right)

        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError

        return operations[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
        return operations[type(node.op)](calculate(node.operand))

    raise ValueError("Invalid calculation")


def get_result():
    tree = ast.parse(expression, mode="eval")
    return calculate(tree.body)


# Update calculator display
def update_display():
    display.config(text=expression if expression else "0")

    try:
        result = get_result()
        preview.config(text="= " + str(result))
    except Exception:
        preview.config(text="")


# Add numbers and operators
def press(value):
    global expression

    if value == "AC":
        expression = ""

    elif value == "⌫":
        expression = expression[:-1]

    elif value == "=":
        try:
            result = get_result()
            expression = str(result)
        except ZeroDivisionError:
            expression = ""
            display.config(text="Cannot divide by zero")
            preview.config(text="")
            return
        except Exception:
            preview.config(text="Invalid expression")
            return

    else:
        expression += value

    update_display()


# Header
header = tk.Label(
    root,
    text="PYTHON CALCULATOR",
    font=("Arial", 20, "bold"),
    bg="#49E675",
    fg="#000000"
)
header.pack(pady=20)

# Main display
display = tk.Label(
    root,
    text="0",
    font=("Arial", 30, "bold"),
    bg="#29DA5E",
    fg="white",
    anchor="e",
    padx=15,
    pady=20
)
display.pack(fill="x", padx=15)

# Live result preview
preview = tk.Label(
    root,
    text="",
    font=("Arial", 18),
    bg="#25334B",
    fg="#34D399",
    anchor="e",
    padx=15
)
preview.pack(fill="x", padx=15)

# Calculator buttons
buttons = [
    ["AC", "⌫", "/", "*"],
    ["7", "8", "9", "-"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["0", ".", "", ""]
]

button_frame = tk.Frame(root, bg="#172033")
button_frame.pack(expand=True, fill="both", padx=12, pady=15)

for r, row in enumerate(buttons):
    for c, value in enumerate(row):
        if not value:
            continue

        color = "#2563EB" if value in ["+", "-", "*", "/", "="] else "#293951"

        if value == "AC":
            color = "#B45353"

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 18, "bold"),
            bg=color,
            fg="red",
            activebackground="#475569",
            activeforeground="Black",
            relief="flat",
            command=lambda v=value: press(v)
        )

        button.grid(
            row=r,
            column=c,
            sticky="nsew",
            padx=5,
            pady=5
        )

for i in range(5):
    button_frame.rowconfigure(i, weight=1)

for i in range(4):
    button_frame.columnconfigure(i, weight=1)

# Start application
root.mainloop()
