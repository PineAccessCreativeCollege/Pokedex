import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk


window_open=False
def open_profile(root):
    global window_open
    print(window_open)
    ######
    #Profile Window
    ######
    
    print("HEy")
    profile = ctk.CTkToplevel( root )
    profile.transient( root )
    
    
    ##SETUP WINDOW
    profile.geometry("500x800")
    profile.overrideredirect(True)  # Remove title bar and "X" button

    profile.grid_columnconfigure(0, weight=1)
    profile.grid_columnconfigure(1, weight=0)
    
    ##FUNCTIONS
    def on_close():
        global window_open
        window_open=False
        print(window_open)
        profile.destroy()
        
    def start_drag(event):
        # Record the initial position when the mouse is pressed
        global drag_data
        drag_data = {'x': event.x, 'y': event.y}

    def do_drag(event):
        # Calculate the movement and move the window
        delta_x = event.x - drag_data['x']
        delta_y = event.y - drag_data['y']
        new_x = profile.winfo_x() + delta_x
        new_y = profile.winfo_y() + delta_y
        profile.geometry(f'+{new_x}+{new_y}')

    
    ##FRAMES
    top_bar = ctk.CTkFrame(profile, height=120, bg_color="transparent")#fg_color="transparent"

    ##IMAGES
    ximagemage_path = "Red_X.png"
    pill_image = Image.open(ximagemage_path).resize((25,25))
    XImage = ImageTk.PhotoImage(pill_image)
    
    ##BUTTONS
    close_button = ctk.CTkButton(top_bar, text=None, width=70, bg_color="transparent", image=XImage,
                                 fg_color="transparent", text_color="red", hover=None, command=on_close)
    
    top_bar.bind("<ButtonPress-1>", start_drag)  # When mouse button is pressed
    top_bar.bind("<B1-Motion>", do_drag)  # When mouse is moved with button pressed
    
    ##LAYOUT
    top_bar.grid(row=0, column=0, sticky="ew")
    close_button.grid(row=0, column=0, sticky="e")
    
    profile.mainloop()
    
    