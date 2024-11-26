import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import requests
from io import BytesIO


class ValentineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Will You Go Out With Me?")
        self.root.geometry("600x700")
        self.root.configure(bg='#F8C8DC')

        # Create main frame
        self.main_frame = tk.Frame(root, bg='#F8C8DC')
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Header text
        self.header = tk.Label(
            self.main_frame,
            text="Do you wanna go out with me?",
            font=('Nunito', 40, 'bold'),
            fg='white',
            bg='#F8C8DC'
        )
        self.header.pack(pady=(10, 20))

        # Load and display GIF
        self.load_gif()

        # Button frame
        self.button_frame = tk.Frame(self.main_frame, bg='#F8C8DC')
        self.button_frame.pack(pady=20)

        # Yes button
        self.yes_button = tk.Button(
            self.button_frame,
            text="Yes",
            command=self.on_yes_click,
            bg='#FFB6C1',
            fg='white',
            font=('Arial', 16),
            width=10,
            borderwidth=0,
            highlightthickness=0
        )
        self.yes_button.pack(side=tk.LEFT, padx=10)

        # No button
        self.no_button = tk.Button(
            self.button_frame,
            text="No",
            bg='#FFB6C1',
            fg='white',
            font=('Arial', 16),
            width=10,
            borderwidth=0,
            highlightthickness=0
        )
        self.no_button.pack(side=tk.LEFT, padx=10)

        # Bind mouse hover event to move the No button
        self.no_button.bind('<Enter>', self.move_no_button)

    def load_gif(self):
        # Download and display GIF
        try:
            gif_url = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDdtZ2JiZDR0a3lvMWF4OG8yc3p6Ymdvd3g2d245amdveDhyYmx6eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/cLS1cfxvGOPVpf9g3y/giphy.gif"
            response = requests.get(gif_url)
            gif_data = Image.open(BytesIO(response.content))

            # Resize the image to fit the window
            gif_data = gif_data.resize((300, 300), Image.LANCZOS)

            # Convert gif to PhotoImage
            gif_photo = ImageTk.PhotoImage(gif_data)

            # Create label to display gif
            self.gif_label = tk.Label(
                self.main_frame,
                image=gif_photo,
                bg='#F8C8DC'
            )
            self.gif_label.image = gif_photo  # Keep a reference
            self.gif_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading GIF: {e}")
            # Fallback text if GIF fails to load
            self.gif_label = tk.Label(
                self.main_frame,
                text="😍",
                font=('Arial', 100),
                bg='#F8C8DC'
            )
            self.gif_label.pack(pady=20)

    def move_no_button(self, event=None):
        # Get window dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Get button dimensions
        button_width = self.no_button.winfo_reqwidth()
        button_height = self.no_button.winfo_reqheight()

        # Ensure the button moves within the window
        x = random.randint(0, max(0, window_width - button_width))
        y = random.randint(0, max(0, window_height - button_height - 200))  # Leave some space at bottom

        # Move the no button using place geometry manager
        self.no_button.place(x=x, y=y)

    def on_yes_click(self):
        # Show a sweet message on yes
        messagebox.showinfo(
            "Yay!",
            "Awesome! I'm so happy you said yes! 💕"
        )
        self.root.quit()


def main():
    root = tk.Tk()
    app = ValentineApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()