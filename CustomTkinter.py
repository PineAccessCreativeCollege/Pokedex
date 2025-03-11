import customtkinter as ctk
from tkinter import PhotoImage, simpledialog, messagebox
from PIL import Image, ImageTk
import Login
import Search
import pandas as pd

class Main(ctk.CTkFrame):
    def __init__(self, master, width = 500, height = 800, corner_radius = None, border_width = None,
                 bg_color = "transparent", fg_color = None, border_color = None,
                 background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color,
                         border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
                    
        ######
        #Root Window Settings
        ######

        self.clicks = 0
        self.previous_click = None  # To store the first clicked button
        self.first_click_button = None  # Store the first button clicked

        self.logged_in = False
        self.user_UUID = "None"
        
        self.profile_window = None
        
        def on_close():
            print("Killing Window")
            self.master.destroy()
            
        def open_profile_window():
            if self.profile_window is None or not self.profile_window.winfo_exists():
                print("Opening Profile Window")
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
        self.search_box = ctk.CTkEntry(self, width=400, height=50, placeholder_text="Enter a Pokemon name or ID")
        
        ##LAYOUT
        top_bar.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=0, sticky="w", padx=(0,370))
        profile_button.grid(row=0, column=1, sticky="e", pady=10, padx=0)
        self.search_box.grid(row=1, column=0, pady=20)
        pokemon_profile.grid(row=2, column=0, sticky="w", padx=10)
        search_results_f.grid(row=2, column=0, sticky="e", padx=10)
        current_party.grid(row=4, column=0, sticky="ew", padx=10, pady=5)    
        
        ##A simple algorithm for filling the buttons up inside the users party/ should
        #make it easier to shift to a class based system for the buttons which should
        #let them be changed on the fly and after login.
        iterated_row = 0
        iterated_column = 0
        
        self.poke_slots = []
        for i in range(6):
            self.poke_slot = ctk.CTkButton(current_party, height=140, text=f"Pokemon {i+1}", command=lambda i=i: self.get_search_click(self.poke_slots[i]))
            if i == 3:
                iterated_row = 1
                iterated_column = 0
            self.poke_slot.grid(row=iterated_row, column=iterated_column, padx=10, pady=10)
            self.poke_slots.append(self.poke_slot)
            iterated_column+=1
            
        i=0
        ##An simpler algorithm for filling the search results frame with buttons
        #for i in range(10):
            #self.i_search_slot = 'search_result_' + str(i)
            #self.i_search_slot = ctk.CTkButton(search_results_f, text=None)
            
            #self.i_search_slot.grid(row=i, column=0, padx=10, pady=10)
            
        self.search_result_buttons = []  # Add this line to store the buttons
        for i in range(10):
            search_slot = ctk.CTkButton(search_results_f, text=f"Result {i+1}", command=lambda i=i: self.get_search_click(self.search_result_buttons[i]))
            search_slot.grid(row=i, column=0, padx=10, pady=10)
            self.search_result_buttons.append(search_slot)
        
    def on_profile_close(self):
        print("Profile window closed")
        self.profile_window.destroy()
        self.profile_window = None
        
    def get_username(self):
        return self.search_box.get()
    
    def get_search_click(self, button):
            """
            Handles the click logic for search results and swapping Pokemon names.
            Tracks clicks and performs the swap if two different Pokemon slots are clicked.
            """
            self.clicks += 1
            print(f"Click count: {self.clicks}")

            if self.clicks == 1:
                # First click - store the button clicked and text
                self.previous_click = button
                self.first_click_button = button
                print(f"First click: {self.previous_click.cget('text')}")
            elif self.clicks == 2:
                # Second click - check if it's the same button clicked
                if self.previous_click != button:
                    # Swap the names
                    print("Swapping Pokémon names")
                    first_text = self.previous_click.cget("text")
                    second_text = button.cget("text")
                    #self.update_poke_slots(self.previous_click, second_text)
                    self.update_poke_slots(button, first_text)
                    self.clicks = 0  # Reset the click counter
                else:
                    print("You clicked the same slot twice!")
                    self.clicks = 0  # Reset the counter on same click

    def update_poke_slots(self, button, text):
        """
        Updates the text of a button in the Pokemon slots.
        """
        button.configure(text=text)
        print(f"Updated {button.cget('text')} to {text}")

    def send_login_register_commands(self, username, password, type):
        print(self.logged_in, self.user_UUID)
        if type == "login":
            self.logged_in, self.user_UUID = Login.Login(username, password)
        elif type == "register":
            self.logged_in, self.user_UUID = Login.Register(username, password)
        else:
            print("Invalid login/register type")
        print(self.logged_in, self.user_UUID)
        
        if self.logged_in:
            self.profile_window.login_window.destroy()
            #Output message box for successful login
            #Run function for fetching user data and filling boxes
            pass
        else:
            self.profile_window.login_window.update_user(self.user_UUID)
            pass
    
    def load_user_data(self):
        # Fetch user data and fill boxes
        # Build modularly for universal use. (or not)
        pass

    def UpdateSearchResults(self, top_results):
        
        try: 
            top_results.isalpha()
            self.search_result_buttons[0].configure(text = top_results)
            return
        except:
            # If there are no results, clear the search results frame
            # Fetch updated search results and fill search results frame
            # Build modularly for universal use. (or not)
            print("Updating Search Results")
            for i, result in enumerate(top_results[:10]):  # Limit to 10 results
                if i < len(self.search_result_buttons):
                    self.search_result_buttons[i].configure(text=result)
            
            # If there are fewer than 10 results, clear the remaining buttons
            for i in range(len(top_results), 10):
                if i < len(self.search_result_buttons):
                    self.search_result_buttons[i].configure(text="")
        
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
        
        self.login_window = None
        self.draggable = DraggableWindow(self)
        
        ##FUNCTIONS
        def on_close():
            self.main_instance.on_profile_close()
        
        def open_login_window():
            if self.login_window is None or not self.login_window.winfo_exists():
                print("Opening Login Window")
                self.login_window = LoginWindow(self)
                self.login_window.protocol("WM_DELETE_WINDOW", self.on_login_close)
            else:
                print("Login window already open")
                self.login_window.focus()
                   
        ##FRAMES
        top_bar = ctk.CTkFrame(self, height=120, bg_color="transparent")#fg_color="transparent"

        ##IMAGES
        ximagemage_path = "Red_X.png"
        pill_image = Image.open(ximagemage_path).resize((25,25))
        XImage = ImageTk.PhotoImage(pill_image)
        
        ##BUTTONS
        close_button = ctk.CTkButton(top_bar, text=None, width=70, bg_color="transparent", image=XImage,
                                    fg_color="transparent", text_color="red", hover=None, command=on_close)
        
        login_button = ctk.CTkButton(top_bar, text="Login", width=100, height=50, bg_color="grey", fg_color="red", command=open_login_window)
        
        top_bar.bind("<ButtonPress-1>", self.draggable.start_drag)  # When mouse button is pressed
        top_bar.bind("<B1-Motion>", self.draggable.do_drag)  # When mouse is moved with button pressed
        
        
        
        ##LAYOUT
        top_bar.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=1, sticky="e", padx=(220,0), pady=10)
        login_button.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    def on_login_close(self):
        print("Login window closed")
        self.login_window.destroy()
        self.login_window = None
    
class LoginWindow(ctk.CTkToplevel):
    def __init__(self, profile_instance, *args, fg_color = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.profile_instance = profile_instance
        
        ######
        #Login Window
        ######
                
        ##SETUP WINDOW
        self.geometry("400x300")
        self.overrideredirect(True)  # Remove title bar and "X" button

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.draggable = DraggableWindow(self)
        
        ##FUNCTIONS
        def on_close():
            self.profile_instance.on_login_close()
        
        def login_data_sender():
            username = username_entry.get()
            password = password_entry.get()
            
            user_data = pd.read_csv('user_data.csv')
            user_pass = str(password)
    
            if user_pass.isspace():
                self.update_user("Passwords cannot contain spaces")
            elif len(user_pass) < 8:
                self.update_user("Password should be 8 chars long")
            elif len(user_pass) > 20:
                self.update_user("Passwords should be less than 20 chars ")
            else:
                self.profile_instance.main_instance.send_login_register_commands(username, password, type = "login")
        
        def register_account():
            username = username_entry.get()
            password = password_entry.get()
            
            user_data = pd.read_csv('user_data.csv')
    
            user_name = str(username)
            
            if user_name in user_data['Username'].values:
                self.update_user("Username already exists")
                #Edit info prompts
                return
            user_pass = str(password)
            
            
            if not user_pass:
                self.update_user("Password cannot be empty")
            elif user_pass.isspace():
                self.update_user("Passwords cannot contain spaces")
            elif len(user_pass) < 8:
                self.update_user("Password should be 8 chars long")
            elif len(user_pass) > 20:
                self.update_user("Passwords should be less than 20 chars ")
            elif not any(char.isupper() for char in user_pass):
                self.update_user("Password must contain at least one uppercase letter")
                #Edit info prompts
                pass            
            else:
                self.profile_instance.main_instance.send_login_register_commands(username, password, type = "register")
              
        ##FRAMES
        top_bar = ctk.CTkFrame(self, height=120, bg_color="transparent")#fg_color="transparent"

        ##IMAGES
        ximagemage_path = "Red_X.png"
        pill_image = Image.open(ximagemage_path).resize((25,25))
        XImage = ImageTk.PhotoImage(pill_image)
        
        ##BUTTONS
        close_button = ctk.CTkButton(top_bar, text=None, width=70, bg_color="transparent", image=XImage,
                                    fg_color="transparent", text_color="red", hover=None, command=on_close)
        submit_button = ctk.CTkButton(self, text="Submit", width=100, height=50, bg_color="grey", 
                                      fg_color="red", command=login_data_sender)
        register_button = ctk.CTkButton(self, text="Click to Register with these details", width=100,
                                        hover_color=None, fg_color="transparent", hover=None, 
                                        command=register_account, text_color="red")
        
        ##ENTRYS
        username_entry = ctk.CTkEntry(self, placeholder_text="Enter your username")
        password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Enter your password")
        
        top_bar.bind("<ButtonPress-1>", self.draggable.start_drag)  # When mouse button is pressed
        top_bar.bind("<B1-Motion>", self.draggable.do_drag)  # When mouse is moved with button pressed
        
        ##LABELS
        
        self.user_hint = ctk.CTkLabel(self, text="Hey you")
        
        ##LAYOUT
        top_bar.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=1, sticky="e", padx=(340,0), pady=10)
        username_entry.grid(row=1, column=0, sticky="ew", pady=(30,10), padx=20)
        password_entry.grid(row=2, column=0, sticky="ew", pady=10, padx=20)
        submit_button.grid(row=4, column=0, sticky="ew", pady=10, padx=40)
        self.user_hint.grid(row=3, column=0, sticky="ew", padx=20)
        register_button.grid(row=5, column=0, sticky="ew")
    
    def update_user(self, error):
        self.user_hint.configure(text=error)
        self.user_hint.configure(width="70%")
       
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
    root.overrideredirect(1)
    root.wm_attributes("-transparentcolor", "grey")
    window = Main(root, corner_radius=100)
    window.grid(row=0, column=0)
    
    def get_pokemon_input(event):
        print("Getting pokemon input")
        pokemon = window.get_username()
        print(f"Username: {pokemon}")
        RunSearchPokemon(pokemon)

    def RunSearchPokemon(input):
        pokemon_results = Search.SearchPokemon(input)
        window.UpdateSearchResults(pokemon_results)
    
    window.master.bind('<Return>', get_pokemon_input)
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
    