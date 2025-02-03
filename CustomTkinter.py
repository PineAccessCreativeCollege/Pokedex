import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class Main(ctk.CTkFrame):
    def __init__(self, master, width = 500, height = 800, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        ######
        #Root Window Settings
        ######
        
        self.profile_window = None
        
        def on_close():
            print("Killing Window")
            self.master.destroy()
            
        def open_profile_window():
            print("Opening Profile Window")
            if self.profile_window is None or not self.profile_window.winfo_exists():
                self.profile_window = ProfileWindow(self)
                self.profile_window.protocol("WM_DELETE_WINDOW", self.on_profile_close)
            else:
                print("Profile window already open")
                self.profile_window.focus()
            
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.draggable = DraggableWindow(self.master)
        
        ##FRAMES

        top_bar = ctk.CTkFrame(self, height=90, bg_color="transparent")#fg_color="transparent"
        pokemon_profile = ctk.CTkFrame(self, height=250, width=300, bg_color="transparent")
        search_results_f = ctk.CTkScrollableFrame(self, height=250, width=150, bg_color="transparent")
        current_party = ctk.CTkFrame(self, height=250, bg_color="transparent")
        
        ##IMAGES
        x_imagemage_path = "Red_X.png"
        pill_image = Image.open(x_imagemage_path).resize((25,25))
        XImage = ImageTk.PhotoImage(pill_image)
        
        ##BUTTONS
        close_button = ctk.CTkButton(top_bar, text=None, width=70, image=XImage, bg_color="transparent",
                                    fg_color="transparent", text_color="red", hover=None, command=on_close)
        
        profile_button = ctk.CTkButton(top_bar, width=50, height=50, text=None, 
                                    fg_color="grey", hover=None, corner_radius=25, 
                                    border_width=0, command=open_profile_window)
        
        
        top_bar.bind("<ButtonPress-1>", self.draggable.start_drag)  # When mouse button is pressed
        top_bar.bind("<B1-Motion>", self.draggable.do_drag)  # When mouse is moved with button pressed
        
        ##ENTRYS
        search_box = ctk.CTkEntry(self, width=400, height=50, placeholder_text="Enter a Pokemon name or ID")
        
        ##LAYOUT
        top_bar.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=0, sticky="w", padx=(0,370))
        profile_button.grid(row=0, column=1, sticky="e", pady=10, padx=0)
        search_box.grid(row=1, column=0, pady=20)
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

    def on_profile_close(self):
        print("Profile window closed")
        self.profile_window.destroy()
        self.profile_window = None

class ProfileWindow(ctk.CTkToplevel):
    def __init__(self, main_instance, *args, fg_color = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.main_instance = main_instance
        
        ######
        #Profile Window
        ######
        
        print("HEy")
                
        ##SETUP WINDOW
        self.geometry("400x700")
        self.overrideredirect(True)  # Remove title bar and "X" button

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.draggable = DraggableWindow(self)
        
        ##FUNCTIONS
        def on_close():
            self.main_instance.on_profile_close()
            
        def start_drag(event):
            # Record the initial position when the mouse is pressed
            global drag_data
            drag_data = {'x': event.x, 'y': event.y}

        def do_drag(event):
            # Calculate the movement and move the window
            delta_x = event.x - drag_data['x']
            delta_y = event.y - drag_data['y']
            new_x = self.winfo_x() + delta_x
            new_y = self.winfo_y() + delta_y
            self.geometry(f'+{new_x}+{new_y}')

        
        ##FRAMES
        top_bar = ctk.CTkFrame(self, height=120, bg_color="transparent")#fg_color="transparent"

        ##IMAGES
        ximagemage_path = "Red_X.png"
        pill_image = Image.open(ximagemage_path).resize((25,25))
        XImage = ImageTk.PhotoImage(pill_image)
        
        ##BUTTONS
        close_button = ctk.CTkButton(top_bar, text=None, width=70, bg_color="transparent", image=XImage,
                                    fg_color="transparent", text_color="red", hover=None, command=on_close)
        
        top_bar.bind("<ButtonPress-1>", self.draggable.start_drag)  # When mouse button is pressed
        top_bar.bind("<B1-Motion>", self.draggable.do_drag)  # When mouse is moved with button pressed
        
        ##LAYOUT
        top_bar.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=0, sticky="e", padx=(335,0), pady=10)

class DraggableWindow():
    def __init__(self, window):
        self.window = window
        self.drag_data = {'x': 0, 'y': 0}
    def start_drag(self, event):
        self.drag_data = {'x': event.x, 'y': event.y} 
    
    def do_drag(self, event):
        delta_x = event.x - self.drag_data['x']
        delta_y = event.y - self.drag_data['y']
        new_x = self.window.winfo_x() + delta_x
        new_y = self.window.winfo_y() + delta_y
        self.window.geometry(f'+{new_x}+{new_y}')
    
def main():
    root=ctk.CTk()
    root.overrideredirect(True)  # Remove title bar and "X" button
    window = Main(root)
    window.grid(row=0, column=0)
    root.mainloop()
    
if __name__ == "__main__":
    main()
    