import random
import tkinter as tk
from tkinter import messagebox


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.banned = False

        # Display
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            root,
            textvar=self.display_var,
            font=("Arial", 24),
            justify="right",
            state="readonly",
            bd=10,
        )
        self.display.pack(fill=tk.BOTH, padx=10, pady=10)

        # Button frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Layout
        self.buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "DEL"],
        ]

        for row in self.buttons:
            row_frame = tk.Frame(self.button_frame)
            row_frame.pack(fill=tk.BOTH, expand=True, pady=5)

            for btn_text in row:
                self.create_button(btn_text, row_frame)

    def create_button(self, text, parent):
        if text == "=":
            bg_color = "#51cf66"
            fg_color = "white"
        elif text in ["+", "-", "*", "/"]:
            bg_color = "#ffd93d"
            fg_color = "black"
        elif text == "C":
            bg_color = "#ff6b6b"
            fg_color = "white"
        elif text == "DEL":
            bg_color = "#ff8c42"
            fg_color = "white"
        else:
            bg_color = "#e9ecef"
            fg_color = "black"

        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 18, "bold"),
            bg=bg_color,
            fg=fg_color,
            relief=tk.RAISED,
            bd=2,
            command=lambda: self.on_button_click(text),
        )
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    def on_button_click(self, text):
        if self.banned:
            messagebox.showerror(
                "BANNED", "You are permanently banned from using calculator"
            )
            return

        current = self.display_var.get()

        if text == "C":
            self.display_var.set("0")
        elif text == "DEL":
            if current != "0":
                self.display_var.set(current[:-1] if len(current) > 1 else "0")
        elif text == "=":
            self.calculate()
        else:
            if current == "0" and text != ".":
                self.display_var.set(text)
            else:
                self.display_var.set(current + text)

    def calculate(self):
        try:
            expression = self.display_var.get()
            result = eval(expression)

            # Random ban chance on calculation
            if random.random() < 0.1:  # 10% chance to get banned
                self.banned = True
                messagebox.showerror(
                    "BANNED", "You are permanently banned from using calculator"
                )
                self.display_var.set("0")
                return

            if isinstance(result, float):
                if result == int(result):
                    self.display_var.set(str(int(result)))
                else:
                    self.display_var.set(str(round(result, 10)))
            else:
                self.display_var.set(str(result))
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.display_var.set("0")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
            self.display_var.set("0")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
