import requests
import cv2
from kivy.properties import ObjectProperty
#from ultralytics import YOLO
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.app import App
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import NoTransition  # Import NoTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList



# Load KV files
Builder.load_file('main.kv')
Builder.load_file('login.kv')
Builder.load_file('signup.kv')
Builder.load_file('profile.kv')
Builder.load_file('pet_profile.kv')
Builder.load_file('dashboard.kv')
#Builder.load_file('livefeed.kv')  # Load the live feed KV file
Builder.load_file('profile_tab.kv')
Builder.load_file('about_us.kv')
Builder.load_file('help.kv')
Builder.load_file('user_guide.kv')
Builder.load_file('FAQs.kv')
Builder.load_file('edit_profile.kv')
Builder.load_file('pet_tab.kv')
Builder.load_file('activity_logs.kv')
'''

class LiveFeedScreen(Screen):
    img_widget = ObjectProperty(None)  # Image widget (using ObjectProperty)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Load the YOLO models for dog detection and behavior detection
        self.dog_model = YOLO('dog_model.pt')  # Model for dog detection
        self.behavior_model = YOLO('behavior_model.pt')  # Model for behavior detection

        ip = '192.168.0.102'

        # Construct the RTSP URL dynamically
        self.rtsp_url = f"rtsp://admin:L2A51CBA@{ip}:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
        
        # Create an Image widget for Kivy
        self.img_widget = Image()  
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.img_widget)
        
        # Start capturing video from RTSP stream
        self.capture = cv2.VideoCapture(self.rtsp_url)

        # Schedule the frame update method (30 FPS)
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # 30 FPS
        
        # Add layout to screen
        self.add_widget(layout)

    def update_frame(self, dt):
        ret, frame = self.capture.read()  # Read a frame from the video capture
        if ret:
            # Flip the frame vertically if it's upside down
            frame = cv2.flip(frame, 0)  # Flip vertically

            # Perform object detection with both models (dog detection and behavior detection)
            dog_results = self.dog_model(frame)  # Get results from the dog detection model
            behavior_results = self.behavior_model(frame)  # Get results from the behavior detection model

            # Extract bounding boxes and plot them manually (no labels)
            # Dog detection
            if dog_results[0].boxes is not None:
                for box in dog_results[0].boxes.xyxy:  # Accessing xyxy values (top-left and bottom-right)
                    x1, y1, x2, y2 = box  # Unpacking the coordinates
                    frame = cv2.rectangle(frame, 
                                        (int(x1), int(y1)),  # top-left corner
                                        (int(x2), int(y2)),  # bottom-right corner
                                        (0, 255, 0),  # green box color
                                        2)  # thickness of the box

            # Behavior detection
            if behavior_results[0].boxes is not None:
                for box in behavior_results[0].boxes.xyxy:  # Accessing xyxy values
                    x1, y1, x2, y2 = box  # Unpacking the coordinates
                    frame = cv2.rectangle(frame, 
                                      (int(x1), int(y1)),  # top-left corner
                                      (int(x2), int(y2)),  # bottom-right corner
                                      (0, 0, 255),  # red box color
                                      2)  # thickness of the box

            # Convert the frame to a Kivy-compatible format (RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            buf = frame.tobytes()  # Convert the frame to bytes for Kivy texture

            # Create a texture for Kivy and update the widget's texture
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img_widget.texture = texture  # Update the Image widget with the new texture

    def on_enter(self):
        print(f"Entering Live Feed Screen. RTSP URL: {self.rtsp_url}")

    def on_leave(self):
        self.capture.release()  # Release the capture when leaving the screen

        '''

class ActivityLogsScreen(Screen):
    def add_activity_log(self, time, activity, is_alert=False):
        """Dynamically adds an activity log card."""
        # Create a card for the log
        card = MDCard(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70),
            md_bg_color=(73/255, 54/255, 40/255, 1) if is_alert else (1, 1, 1, 1),
            radius=[dp(10)],
        )

        # Layout to hold the time and activity labels
        layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(70))

        # Add time label
        time_label = MDLabel(
            text=time,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1) if is_alert else (79/255, 54/255, 48/255, 1),
            font_size="16sp",
            halign="center",
            size_hint_x=0.3,
        )
        layout.add_widget(time_label)

        # Add activity label
        activity_label = MDLabel(
            text=activity,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1) if is_alert else (79/255, 54/255, 48/255, 1),
            font_size="16sp",
            halign="center",
            size_hint_x=0.7,
        )
        layout.add_widget(activity_label)

        # Add alert icon if it's an alert
        if is_alert:
            icon_button = MDIconButton(
                icon="alert-circle",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint_x=None,
                size_hint_y=None,
            )
            layout.add_widget(icon_button)

        # Add the layout to the card
        card.add_widget(layout)

        # Now add the card to the MDList (which is inside the ScrollView)
        scroll_list = self.ids.scroll_list  # This assumes you have an MDList with the id 'scroll_list'
        scroll_list.add_widget(card)

    def go_to_live_feed(self):
        self.manager.current = "live_feed"
        
    def profile_tab(self):
        self.manager.current = "profile_tab"

    def home(self):
        self.manager.current = "dashboard"
    
    def pet_tab(self):
        self.manager.current = "pet_tab"
    
    def activity_logs(self):
        self.manager.current = "activity_logs"

class ScreenManagement(ScreenManager):
    pass

class SignupScreen(Screen):
    def signup(self, full_name, email, password):
        # Check for valid email domain
        if not (email.endswith("@yahoo.com") or email.endswith("@gmail.com")):
            self.display_error_message("Please use a @yahoo.com or @gmail.com email.")
            return

        # Check if password meets the minimum length requirement
        if len(password) < 6:
            self.display_error_message("Password must be at least 6 characters long.")
            return

        url = "http://127.0.0.1:8000/api/signup/"
        data = {"full_name": full_name, "email": email, "password": password}

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                # Store the user data for profile tab
                profile_tab_screen = self.manager.get_screen('profile_tab')
                profile_tab_screen.ids.full_name_label.text = full_name
                profile_tab_screen.ids.email_label.text = email

                self.login_after_signup(full_name, email, password)
            else:
                error_message = "Signup failed: " + response.json().get('error', 'Unknown error')
                self.display_error_message(error_message)

        except Exception as e:
            self.display_error_message("An error occurred during signup. Please try again later.")
            print(f"Error during signup: {e}")

    def login_after_signup(self, full_name, email, password):
        url = "http://127.0.0.1:8000/api/login/"
        data = {"email": email, "password": password}

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                dashboard_screen = self.manager.get_screen('dashboard')
                dashboard_screen.ids.user_label.text = f"Hello, [b]{full_name}[/b]"
                self.manager.current = "profile"
            else:
                print("Login after signup failed:", response.json().get('error', 'Unknown error'))

        except Exception as e:
            print(f"Error during login after signup: {e}")

    def display_error_message(self, message):
        # Display error message in a label
        self.ids.label_error.text = message  # Assuming you have a label with the id 'label_error' in your KV file
        print(f"Error: {message}")  # Debug print

class LoginScreen(Screen):
    def login(self, email, password):
        self.ids.label_error.text = ""  # Clear previous error messages

        url = "http://127.0.0.1:8000/api/login/"
        data = {"email": email, "password": password}

        if not email or not password:
            self.ids.label_error.text = "Please enter both email and password."
            return

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                user_data = response.json()
                full_name = user_data.get('full_name')

                # Store the user data for profile tab directly here
                profile_tab_screen = self.manager.get_screen('profile_tab')
                profile_tab_screen.ids.full_name_label.text = full_name
                profile_tab_screen.ids.email_label.text = email

                # Update the dashboard screen with the user's name
                dashboard_screen = self.manager.get_screen('dashboard')
                dashboard_screen.ids.user_label.text = f"Hello, [b]{full_name}[/b]"
                
                # Fetch pet profile and display it on the dashboard
                dashboard_screen.fetch_pet_profile(email)
                
                # Navigate to the dashboard
                self.manager.current = "dashboard"
            else:
                self.ids.label_error.text = response.json().get('error', 'Login failed, please try again.')

        except Exception as e:
            self.ids.label_error.text = f"Error during login: {e}"



class ProfileScreen(Screen):
    def on_enter(self, *args):
        # Retrieve full_name and email from the 'signup' screen
        full_name = self.manager.get_screen('signup').ids.full_name.text
        email = self.manager.get_screen('signup').ids.email.text
        
        # Update the Labels instead of TextInput to display the data
        self.ids.full_name_label.text = full_name
        self.ids.email_label.text = email


class PetProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "text": "Male",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Male": self.set_gender(x),
            },
            {
                "text": "Female",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Female": self.set_gender(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.gender_dropdown,
            items=menu_items,
            width_mult=3,
        )

    def open_gender_menu(self):
        self.menu.open()

    def set_gender(self, gender):
        self.ids.gender_dropdown.text = gender
        self.menu.dismiss()

    def save_pet_profile(self):
        # Get values from the input fields
        pet_name = self.ids.pet_name_input.text
        pet_breed = self.ids.pet_breed_input.text
        pet_age = self.ids.pet_age_input.text
        gender = self.ids.gender_dropdown.text

        if not pet_name or not pet_breed or not pet_age or gender == "Select Gender":
            print("Please fill in all fields before saving.")
            return

        self.submit_pet_profile_to_api(pet_name, pet_breed, pet_age, gender)

    def submit_pet_profile_to_api(self, pet_name, pet_breed, pet_age, gender):
        url = "http://127.0.0.1:8000/api/pet_profile/"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        data = {
            "pet_name": pet_name,
            "pet_breed": pet_breed,
            "pet_age": pet_age,
            "gender": gender
        }

        try:
            print(f"Sending request to {url} with data: {data}")  # Debug print
            response = requests.post(url, json=data, headers=headers)
            
            print(f"Response status code: {response.status_code}")  # Debug print
            print(f"Response content: {response.text}")  # Debug print
            
            if response.status_code == 201:
                print("Pet profile saved successfully!")
                # Update dashboard screen immediately after saving
                dashboard_screen = self.manager.get_screen('dashboard')
                dashboard_screen.ids.pet_name_label.text = f"Name: {pet_name}"
                dashboard_screen.ids.pet_breed_label.text = f"Breed: {pet_breed}"
                dashboard_screen.ids.pet_age_label.text = f"Age: {pet_age}"
                dashboard_screen.ids.pet_gender_label.text = f"Gender: {gender}"
                
                self.manager.current = "dashboard"  # Navigate to dashboard screen
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error during saving pet profile: {str(e)}")

class DashboardScreen(Screen):
    def fetch_pet_profile(self, email):
        url = f"http://127.0.0.1:8000/api/pet_profile/?email={email}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                pet_profile = response.json()
                
                # Update labels with fetched pet profile data
                self.ids.pet_name_label.text = f"Name: {pet_profile['pet_name']}"
                self.ids.pet_breed_label.text = f"Breed: {pet_profile['pet_breed']}"
                self.ids.pet_age_label.text = f"Age: {pet_profile['pet_age']}"
                self.ids.pet_gender_label.text = f"Gender: {pet_profile['gender']}"
                
                print("Pet profile loaded successfully!")
            else:
                print("Failed to load pet profile:", response.json().get('error', 'Unknown error'))
        except Exception as e:
            print(f"Error fetching pet profile: {e}")


    def go_to_live_feed(self):
        self.manager.current = "live_feed"

    def profile_tab(self):
        self.manager.current = "profile_tab"

    def home(self):
        self.manager.current = "dashboard"
    
    def pet_tab(self):
        self.manager.current = "pet_tab"
    
    def activity_logs(self):
        self.manager.current = "activity_logs"

class PetTabScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {
                "text": "Male",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Male": self.set_gender(x),
            },
            {
                "text": "Female",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Female": self.set_gender(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.gender_dropdown,
            items=menu_items,
            width_mult=3,
        )

    def open_gender_menu(self):
        self.menu.open()

    def set_gender(self, gender):
        self.ids.gender_dropdown.text = gender
        self.menu.dismiss()
        
    def pet_tab(self):
        self.manager.current = "pet_tab"
    
    def profile_tab(self):
        self.manager.current = "profile_tab"
    
    def home(self):
        self.manager.current = "dashboard"
    
    def go_to_live_feed(self):
        self.manager.current = "live_feed"
    


class ProfileTabScreen(Screen):
    def on_enter(self, *args):
        # No need to fetch data from other screens, as it’s set directly
        if not self.ids.full_name_label.text:
            self.ids.full_name_label.text = "No name available"
        if not self.ids.email_label.text:
            self.ids.email_label.text = "No email available"
    
    def go_to_live_feed(self):
        self.manager.current = "live_feed"
    
    def profile_tab(self):
        self.manager.current = "profile_tab"

    def home(self):
        self.manager.current = "dashboard"
    
    def pet_tab(self):
        self.manager.current = "pet_tab"

class AboutUsScreen(Screen):
    pass

class HelpScreen(Screen):
    pass

class UserGuideScreen(Screen):
    pass

class FAQsScreen(Screen):
    pass


class EditProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        # Load current user data into the edit fields
        profile_tab_screen = self.manager.get_screen('profile_tab')
        self.ids.edit_full_name_input.text = profile_tab_screen.ids.full_name_label.text
        self.ids.edit_email_input.text = profile_tab_screen.ids.email_label.text

    def save_changes(self):
        # Get updated input values
        current_email = self.manager.get_screen('profile_tab').ids.email_label.text
        new_full_name = self.ids.edit_full_name_input.text.strip()
        new_email = self.ids.edit_email_input.text.strip()

        print(f"Attempting to update profile with name: {new_full_name}, email: {new_email}")  # Debug print

        # Validate inputs
        if not new_full_name or not new_email:
            self.show_popup("Please fill in all fields!")
            return

        if not (new_email.endswith("@yahoo.com") or new_email.endswith("@gmail.com")):
            self.show_popup("Please use a valid @yahoo.com or @gmail.com email.")
            return

        # Prepare data for API request
        url = "http://127.0.0.1:8000/api/update_profile/"
        data = {
            "current_email": current_email,
            "new_full_name": new_full_name,
            "new_email": new_email
        }

        # Send request
        try:
            print(f"Sending request to {url} with data: {data}")  # Debug print
            response = requests.put(url, json=data)
            print(f"Response status: {response.status_code}")  # Debug print

            if response.status_code == 200:
                # Success: Update profile information across screens
                self.update_profile_information(new_full_name, new_email)
                self.show_popup("Profile updated successfully!")
                Clock.schedule_once(lambda dt: self.return_to_profile(), 1)
            else:
                # Handle errors from the server
                error_message = response.json().get("error", "Failed to update profile")
                self.show_popup(f"Error: {error_message}")

        except requests.exceptions.RequestException as e:
            print(f"Request exception: {str(e)}")  # Debug print
            self.show_popup("Network error. Please check your connection.")

        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Debug print
            self.show_popup(f"An error occurred: {str(e)}")

    def update_profile_information(self, new_full_name, new_email):
        try:
            # Update ProfileTabScreen
            profile_tab_screen = self.manager.get_screen('profile_tab')
            profile_tab_screen.ids.full_name_label.text = new_full_name
            profile_tab_screen.ids.email_label.text = new_email

            # Update Dashboard
            dashboard_screen = self.manager.get_screen('dashboard')
            dashboard_screen.ids.user_label.text = f"Hello, [b]{new_full_name}[/b]"

            print("Profile information updated successfully")  # Debug print
        except Exception as e:
            print(f"Error updating profile information: {str(e)}")  # Debug print
            raise

    def return_to_profile(self):
        self.manager.current = "profile_tab"

    def show_popup(self, message):
        popup = Popup(
            title="Message",
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()
        print(f"Showing popup with message: {message}")  # Debug print

    def cancel_changes(self):
        self.manager.current = "profile_tab"



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        print("MainScreen initialized")

class PetWatch(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None  # Initialize dialog to None

    def build(self):
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(MainScreen(name="main"))
        screen_manager.add_widget(LoginScreen(name="login"))
        screen_manager.add_widget(SignupScreen(name="signup"))
        screen_manager.add_widget(ProfileScreen(name="profile"))
        screen_manager.add_widget(PetProfileScreen(name="pet_profile"))
        screen_manager.add_widget(DashboardScreen(name="dashboard"))
        #screen_manager.add_widget(LiveFeedScreen(name="live_feed"))
        screen_manager.add_widget(PetTabScreen(name="pet_tab"))
        screen_manager.add_widget(ActivityLogsScreen(name="activity_logs"))
        screen_manager.add_widget(ProfileTabScreen(name="profile_tab"))
        screen_manager.add_widget(AboutUsScreen(name="about_us"))
        screen_manager.add_widget(HelpScreen(name="help_button"))
        screen_manager.add_widget(EditProfileScreen(name="edit_profile"))
        screen_manager.add_widget(UserGuideScreen(name="userguide"))
        screen_manager.add_widget(FAQsScreen(name="faqs"))


        if hasattr(Window, 'metrics'):
            density = Window.metrics['density']
            print(f"Screen density: {density}")
        else:
            print("Window.metrics not available, using default density of 1")
            density = 1

        scaled_padding = 10 * density
        print(f"Scaled padding: {scaled_padding}")

        return screen_manager

    def next_step(self):
        self.root.current = "pet_profile"

    def prev_step(self):
        self.root.current = "profile"

    def next_step_dash(self):
        self.root.current = "dashboard"
    
    def goto_about_us(self):
        # Switch to the "about_us" screen
        self.root.current = "about_us"
    
    def activity_logs(self):
        self.root.current = "activity_logs"
    
    def goto_help(self):
        # Switch to the "about_us" screen
        self.root.current = "help_button"
    
    def cancel_changes(self):
        # This function switches the screen back to 'profile_tab'
        self.root.current = "profile_tab"

    def show_logout_confirmation(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Are you sure you want to log out?",
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=self.close_dialog
                    ),
                    MDRaisedButton(
                        text="LOG OUT",
                        on_release=self.logout
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj=None):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None  # Reset dialog to None after dismissing

    def logout(self, obj=None):
        self.close_dialog()  # Close the dialog
        print("Logging out...")
        self.root.current = "login"  # Redirect to login screen


if __name__ == "__main__":
    LabelBase.register(name="BPoppins", fn_regular="fonts/Poppins/Poppins-SemiBold.ttf")
    LabelBase.register(name="MPoppins", fn_regular="fonts/Poppins/Poppins-Medium.ttf")
    PetWatch().run()