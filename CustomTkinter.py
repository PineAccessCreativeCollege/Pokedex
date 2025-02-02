import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def main():
    
    
    
    
    root = ctk.CTk(screenName=None, baseName=None, useTk=1)
    
    def on_close():
        print("Close button disabled")
        root.destroy()
        
    def start_drag(event):
        # Record the initial position when the mouse is pressed
        global drag_data
        drag_data = {'x': event.x, 'y': event.y}

    def do_drag(event):
        # Calculate the movement and move the window
        delta_x = event.x - drag_data['x']
        delta_y = event.y - drag_data['y']
        new_x = root.winfo_x() + delta_x
        new_y = root.winfo_y() + delta_y
        root.geometry(f'+{new_x}+{new_y}')

    
    root.geometry("500x800")
    root.overrideredirect(True)  # Remove title bar and "X" button

    root.grid_columnconfigure(0, weight=1)

    top_bar = ctk.CTkFrame(root, height=90, bg_color="transparent")#fg_color="transparent"
    top_bar.grid(row=0, sticky="ew")
    
    ##Define Custom X button
    XImage_path = "Red_X.png"
    XImage = PhotoImage(file=XImage_path)
    
    XImage_path = Image.open('Red_X.png').resize((25,25))
    XImage = ImageTk.PhotoImage(XImage_path)
    
    close_button = ctk.CTkButton(top_bar, text=None, width=70,image=XImage, bg_color="transparent",fg_color="transparent",
                                 text_color="red", hover=None, command=on_close)
    close_button.grid()
    
    profile_button = ctk.CTkButton(top_bar)
    profile_button.grid(column=8, row=0, sticky="e")

    top_bar.bind("<ButtonPress-1>", start_drag)  # When mouse button is pressed
    top_bar.bind("<B1-Motion>", do_drag)  # When mouse is moved with button pressed

    w = ctk.CTkEntry(root, width=400, height=50)
    w.grid(row=10, pady=20)

    root.mainloop()
    
if __name__ == "__main__":
    main()