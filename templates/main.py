import re
import tkinter
import tkinter.messagebox

import threading
from time import sleep
import customtkinter
import json
import os


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class Gui(customtkinter.CTk):
    # Driver setup
    driver = None

    def __init__(self):
        super().__init__()

        # Gui setup
        self.title("Form Robot")
        self.geometry(f"{550}x{550}")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # current_dir = os.path.dirname(__file__)
        # self.after(201, lambda: self.iconbitmap(os.path.join(current_dir, "FU.ico")))

        self.frame_1 = customtkinter.CTkFrame(master=self)
        self.frame_1.pack(pady=20, padx=40, fill="both", expand=True)

        self.DateEntry = customtkinter.CTkEntry(master=self.frame_1, placeholder_text="Fatura Tarihi")
        self.DateEntry.pack(pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(
            master=self.frame_1,
            command=self.dummy2,
            text="Kaydet",
        )
        self.button_1.pack(pady=10, padx=10)

        # self.Console = customtkinter.CTkTextbox(master=self.frame_1, width=500, height=500)
        # self.Console.pack(pady=10, padx=10)

    def is_valid_number(input_str):
        # Define a regular expression pattern to match valid numbers
        # This pattern allows positive and negative numbers, and floating-point numbers
        number_pattern = r"^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"

        # Use re.match to check if the input matches the number pattern
        return bool(re.match(number_pattern, input_str))

    def on_closing(self):
        """Called when you press the X button to close the program. Kills the GUI and the opened chromedriver threads"""
        if self.driver is not None:
            try:
                self.driver.close()
            except Exception as e:
                # Handle any exception that occurs when trying to close the driver
                print(f"Error while closing the driver: {e}")
            if self.driver.session_id:
                self.driver.quit()
        self.destroy()

    def dummy2(self):
        pass

    def dummy3(self):
        pass


if __name__ == "__main__":
    # initate the gui
    FR = Gui()
    # start the gui
    FR.mainloop()
