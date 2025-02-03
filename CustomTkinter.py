import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import Profile
from Profile import window_open
from Profile import open_profile

def main():    
    ######
    #Root Window
    ######
       
    root = ctk.CTk(screenName=None, baseName=None, useTk=1)
    window_open=False
    
    def on_close():
        print("Killing Window")
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
    root.grid_columnconfigure(1, weight=0)
    
    def open_profile_root():
        window_open=False
        if window_open == False:
            print("Window Open")
            Profile.open_profile(root)
        else:
            print("Window not")
            

    ##FRAMES

    top_bar = ctk.CTkFrame(root, height=90, bg_color="transparent")#fg_color="transparent"
    pokemon_profile = ctk.CTkFrame(root, height=250, width=300, bg_color="transparent")
    search_results_f = ctk.CTkScrollableFrame(root, height=250, width=150, bg_color="transparent")
    current_party = ctk.CTkFrame(root, height=250, bg_color="transparent")
    
    ##IMAGES
    ximagemage_path = "Red_X.png"
    pill_image = Image.open(ximagemage_path).resize((25,25))
    XImage = ImageTk.PhotoImage(pill_image)
    
    ##BUTTONS
    close_button = ctk.CTkButton(top_bar, text=None, width=70, image=XImage, bg_color="transparent",
                                 fg_color="transparent", text_color="red", hover=None, command=on_close)
    
    profile_button = ctk.CTkButton(top_bar, width=50, height=50, text=None, 
                                   fg_color="grey", hover=None, corner_radius=25, 
                                   border_width=0, command=open_profile_root)
    
    
    top_bar.bind("<ButtonPress-1>", start_drag)  # When mouse button is pressed
    top_bar.bind("<B1-Motion>", do_drag)  # When mouse is moved with button pressed
     
    ##ENTRYS
    search_box = ctk.CTkEntry(root, width=400, height=50, placeholder_text="Enter a Pokemon name or ID")
    
    ##LAYOUT
    top_bar.grid(row=0, column=0, sticky="ew")
    close_button.grid(row=0, column=0, sticky="w")
    profile_button.grid(row=0, column=1, sticky="e", padx=370, pady=10)
    search_box.grid(row=1, columnspan=2, pady=20)
    pokemon_profile.grid(row=2, column=0, sticky="w", padx=10)
    search_results_f.grid(row=2, column=0, sticky="e", padx=10)
    current_party.grid(row=3, column=0, sticky="ew", padx=10, pady=20)
    
    
    ##A simple algorithm for filling the buttons up inside the users party/ should
    #make it easier to shift to a class based system for the buttons which should
    #let them be changed on the fly and after login.
    iterated_row = 0
    iterated_column = 0
    
    for i in range(6):
        i_poke_slot = 'pokemon_slot_' + str(i)
        i_poke_slot = ctk.CTkButton(current_party, height=140, text=None)
        if i == 3:
            iterated_row = 1
            iterated_column = 0
        i_poke_slot.grid(row=iterated_row, column=iterated_column, padx=10, pady=10)
        iterated_column+=1
        
        
    ##An simpler algorithm for filling the search results frame with buttons
    for i in range(10):
        i_search_slot = 'search_result_' + str(i)
        i_search_slot = ctk.CTkButton(search_results_f, text=None)
        
        i_search_slot.grid(row=i, column=0, padx=10, pady=10)    
    
    ##Runs the Main Window
        
    root.mainloop()
    
if __name__ == "__main__":
    main()