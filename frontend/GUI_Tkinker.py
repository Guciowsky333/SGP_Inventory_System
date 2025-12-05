import tkinter as tk
import requests
from requests.auth import HTTPBasicAuth
import json


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # API Configuration
        self.BASE_URL = "http://127.0.0.1:8000/api"
        self.auth = None
        self.is_admin = False

        self.window_setup()
        self.create_widgets()
        self.setup_bindings()
        self.entry_login.focus_set()

    # Main window setup
    def window_setup(self):
        self.title('Warehouse System J.sgp')
        self.config(bg='black')

        # Window dimensions and centering
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Create all frames and widgets
    def create_widgets(self):
        # ========== FRAMES ==========
        self.frame_login = tk.Frame(self, bg='black')
        self.frame_login.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_logged_in = tk.Frame(self, bg='black')
        self.frame_logged_in.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_add = tk.Frame(self, bg='black')
        self.frame_add.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_release = tk.Frame(self, bg='black')
        self.frame_release.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_show_component = tk.Frame(self, bg='black')
        self.frame_show_component.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_show_localization = tk.Frame(self, bg='black')
        self.frame_show_localization.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.frame_admin = tk.Frame(self, bg='black')
        self.frame_admin.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ========== LOGIN FRAME ==========
        tk.Label(self.frame_login, text='Login:', bg='black', fg='green',
                 font=('Arial', 16)).place(x=238, y=165)
        self.entry_login = tk.Entry(self.frame_login, bg='black', fg='green', width=12,
                                    insertbackground='green', bd=0, highlightthickness=0,
                                    font=('Arial', 16))
        self.entry_login.place(x=306, y=167)
        tk.Frame(self.frame_login, bg='green', width=146, height=2).place(x=306, y=190)

        tk.Label(self.frame_login, text='Password:', bg='black', fg='green',
                 font=('Arial', 16)).place(x=238, y=202)
        self.entry_password = tk.Entry(self.frame_login, bg='black', fg='green', width=9,
                                       insertbackground='green', bd=0, highlightthickness=0,
                                       font=('Arial', 16), show='*')
        self.entry_password.place(x=347, y=204)
        tk.Frame(self.frame_login, bg='green', width=105, height=2).place(x=347, y=227)

        self.label_login_error = tk.Label(self.frame_login, text='', bg='black', fg='red',
                                          font=('Arial', 11))
        self.label_login_error.place(x=230, y=235)

        # ========== LOGGED IN FRAME ==========
        tk.Label(self.frame_logged_in, text='Welcome to "Warehouse System"', bg='black',
                 fg='green', font=('Arial', 20)).place(x=10, y=5)
        tk.Label(self.frame_logged_in, text='Choose what you want to do:', bg='black',
                 fg='green', font=('Arial', 20)).place(x=10, y=40)

        self.btn_add = tk.Button(self.frame_logged_in, text='Add Component          ',
                                 bg='yellow', fg='black', font=('Arial', 15),
                                 command=self.show_add_frame)
        self.btn_add.place(x=10, y=90)

        self.btn_release = tk.Button(self.frame_logged_in, text='Release Component      ',
                                     bg='yellow', fg='black', font=('Arial', 15),
                                     command=self.show_release_frame)
        self.btn_release.place(x=10, y=140)

        self.btn_show_component = tk.Button(self.frame_logged_in, text='Show Component Location',
                                            bg='yellow', fg='black', font=('Arial', 15),
                                            command=self.show_component_frame)
        self.btn_show_component.place(x=10, y=190)

        self.btn_show_localization = tk.Button(self.frame_logged_in, text='Show Localization Stock',
                                               bg='yellow', fg='black', font=('Arial', 15),
                                               command=self.show_localization_frame)
        self.btn_show_localization.place(x=10, y=240)

        # ========== ADD COMPONENT FRAME ==========
        tk.Label(self.frame_add, text='Enter component data to add:', bg='black', fg='green',
                 font=('Arial', 30)).place(x=10, y=30)
        tk.Frame(self.frame_add, bg='green', width=800, height=4).place(x=0, y=87)

        tk.Label(self.frame_add, text='Code:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=10, y=110)
        self.entry_add_code = tk.Entry(self.frame_add, bg='black', fg='green', width=4,
                                       insertbackground='green', bd=0, highlightthickness=0,
                                       font=('Arial', 16))
        self.entry_add_code.place(x=95, y=117)
        tk.Frame(self.frame_add, bg='green', width=50, height=2).place(x=95, y=140)

        tk.Label(self.frame_add, text='Localization:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=10, y=150)
        self.entry_add_localization = tk.Entry(self.frame_add, bg='black', fg='green', width=7,
                                               insertbackground='green', bd=0, highlightthickness=0,
                                               font=('Arial', 16))
        self.entry_add_localization.place(x=161, y=157)
        tk.Frame(self.frame_add, bg='green', width=77, height=2).place(x=161, y=180)

        tk.Label(self.frame_add, text='Quantity:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=10, y=190)
        self.entry_add_quantity = tk.Entry(self.frame_add, bg='black', fg='green', width=3,
                                           insertbackground='green', bd=0, highlightthickness=0,
                                           font=('Arial', 16))
        self.entry_add_quantity.place(x=135, y=197)
        tk.Frame(self.frame_add, bg='green', width=40, height=2).place(x=135, y=220)

        self.label_add_message = tk.Label(self.frame_add, text='', bg='black', fg='green',
                                          font=('Arial', 16))
        self.label_add_message.place(relx=0.5, rely=0.5, anchor='center')

        # ========== RELEASE COMPONENT FRAME ==========
        tk.Label(self.frame_release, text='Enter component data to release:', bg='black', fg='green',
                 font=('Arial', 30)).place(x=10, y=30)
        tk.Frame(self.frame_release, bg='green', width=800, height=4).place(x=0, y=87)

        tk.Label(self.frame_release, text='Code:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=10, y=110)
        self.entry_release_code = tk.Entry(self.frame_release, bg='black', fg='green', width=4,
                                           insertbackground='green', bd=0, highlightthickness=0,
                                           font=('Arial', 16))
        self.entry_release_code.place(x=95, y=117)
        tk.Frame(self.frame_release, bg='green', width=50, height=2).place(x=95, y=140)

        tk.Label(self.frame_release, text='Localization:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=10, y=150)
        self.entry_release_localization = tk.Entry(self.frame_release, bg='black', fg='green', width=7,
                                                   insertbackground='green', bd=0, highlightthickness=0,
                                                   font=('Arial', 16))
        self.entry_release_localization.place(x=161, y=157)
        tk.Frame(self.frame_release, bg='green', width=77, height=2).place(x=161, y=180)

        tk.Label(self.frame_release, text='Quantity:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=10, y=190)
        self.entry_release_quantity = tk.Entry(self.frame_release, bg='black', fg='green', width=3,
                                               insertbackground='green', bd=0, highlightthickness=0,
                                               font=('Arial', 16))
        self.entry_release_quantity.place(x=135, y=197)
        tk.Frame(self.frame_release, bg='green', width=40, height=2).place(x=135, y=220)

        self.label_release_message = tk.Label(self.frame_release, text='', bg='black', fg='green',
                                              font=('Arial', 16))
        self.label_release_message.place(relx=0.5, rely=0.5, anchor='center')

        # ========== SHOW COMPONENT LOCATIONS FRAME ==========
        tk.Label(self.frame_show_component, text='Enter code to see locations:', bg='black', fg='green',
                 font=('Arial', 30)).place(x=10, y=30)
        tk.Frame(self.frame_show_component, bg='green', width=800, height=4).place(x=0, y=87)

        tk.Label(self.frame_show_component, text='Component Code:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=100, y=111)
        self.entry_show_code = tk.Entry(self.frame_show_component, bg='black', fg='green', width=4,
                                        insertbackground='green', bd=0, highlightthickness=0,
                                        font=('Arial', 20))
        self.entry_show_code.place(x=348, y=113)
        tk.Frame(self.frame_show_component, bg='green', width=60, height=2).place(x=348, y=145)

        self.label_show_component_message = tk.Label(self.frame_show_component, text='', bg='black',
                                                     fg='green', font=('Courier', 16))
        self.label_show_component_message.place(relx=0.5, rely=0.5, anchor='center')

        # ========== SHOW LOCALIZATION CONTENTS FRAME ==========
        tk.Label(self.frame_show_localization, text='Enter localization name:', bg='black', fg='green',
                 font=('Arial', 30)).place(x=10, y=30)
        tk.Frame(self.frame_show_localization, bg='green', width=800, height=4).place(x=0, y=87)

        tk.Label(self.frame_show_localization, text='Localization:', bg='black', fg='green',
                 font=('Arial', 20)).place(x=100, y=111)
        self.entry_show_localization = tk.Entry(self.frame_show_localization, bg='black', fg='green',
                                                width=6, insertbackground='green', bd=0,
                                                highlightthickness=0, font=('Arial', 20))
        self.entry_show_localization.place(x=295, y=113)
        tk.Frame(self.frame_show_localization, bg='green', width=90, height=2).place(x=295, y=145)

        self.label_show_localization_message = tk.Label(self.frame_show_localization, text='',
                                                        bg='black', fg='green', font=('Courier', 16))
        self.label_show_localization_message.place(relx=0.5, rely=0.5, anchor='center')

        # ========== ADMIN FRAME ==========
        tk.Label(self.frame_admin, text='Welcome Admin Lotnik!', bg='black', fg='green',
                 font=('Arial', 40)).place(x=10, y=10)
        tk.Frame(self.frame_admin, bg='green', width=800, height=6).place(x=0, y=75)
        tk.Label(self.frame_admin, text='Press red button to completely clear warehouse',
                 bg='black', fg='yellow', font=('Arial', 20)).place(x=0, y=100)

        self.btn_clear_warehouse = tk.Button(self.frame_admin, text='Clear Entire Warehouse',
                                             bg='red', fg='white', font=('Arial', 40),
                                             command=self.clear_warehouse)
        self.btn_clear_warehouse.place(relx=0.5, rely=0.5, anchor='center')

        self.label_admin_message = tk.Label(self.frame_admin, text='', bg='black', fg='green',
                                            font=('Arial', 20))
        self.label_admin_message.place(x=150, y=391)

        # Set initial frame
        self.frame_login.tkraise()
        self.current_frame = 'login'

    # ========== API METHODS ==========

    def api_request(self, method, endpoint, data=None):
        """Generic API request handler"""
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url, auth=self.auth, timeout=5)
            elif method == 'POST':
                response = requests.post(url, json=data, auth=self.auth, timeout=5)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, auth=self.auth, timeout=5)
            elif method == 'DELETE':
                response = requests.delete(url, auth=self.auth, timeout=5)

            return response
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.Timeout:
            return None
        except Exception as e:
            return None

    def login_user(self, event=None):
        """Handle user login"""
        username = self.entry_login.get()
        password = self.entry_password.get()

        if not username or not password:
            self.show_message('login', 'Please enter login and password', 'red')
            return

        # Create auth object
        self.auth = HTTPBasicAuth(username, password)

        # Check credentials with /me/ endpoint
        response = self.api_request('GET', 'me/')

        if response is None:
            self.show_message('login', 'Cannot connect to server', 'red')
            self.auth = None
            return

        if response.status_code == 403:
            self.show_message('login', 'Wrong login or password', 'red')
            self.auth = None
            self.entry_login.delete(0, 'end')
            self.entry_password.delete(0, 'end')
            self.entry_login.focus_set()
            return

        if response.status_code == 200:
            data = response.json()
            self.is_admin = data.get('is_superuser', False)

            # Clear login fields
            self.entry_login.delete(0, 'end')
            self.entry_password.delete(0, 'end')

            # Show appropriate frame
            if self.is_admin:
                self.frame_admin.tkraise()
                self.current_frame = 'admin'
            else:
                self.frame_logged_in.tkraise()
                self.current_frame = 'logged_in'

    def add_component(self):
        """Add component to warehouse"""
        code = self.entry_add_code.get()
        localization = self.entry_add_localization.get().upper()
        quantity = self.entry_add_quantity.get()

        # Validation
        if not code or not localization or not quantity:
            self.show_message('add', 'Fill all fields', 'red')
            return

        if len(code) != 4 or not code.isdigit():
            self.show_message('add', 'Code must be 4 digits', 'red')
            self.clear_add_entries()
            return

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            self.show_message('add', 'Quantity must be positive number', 'red')
            self.clear_add_entries()
            return

        # API call
        data = {
            'code': code,
            'localization': localization,
            'quantity': quantity
        }

        response = self.api_request('POST', 'add_components/', data)

        if response is None:
            self.show_message('add', 'Connection error', 'red')
            return

        if response.status_code in [200, 201]:
            result = response.json()
            self.show_message('add', result.get('message', 'Added successfully'), 'blue')
        else:
            try:
                error = response.json()
                if 'message' in error:
                    self.show_message('add', error['message'], 'red')
                else:
                    # Handle validation errors
                    error_msg = self.format_error(error)
                    self.show_message('add', error_msg, 'red')
            except:
                self.show_message('add', f'Error: {response.status_code}', 'red')

        self.clear_add_entries()

    def release_component(self):
        """Release component from warehouse"""
        code = self.entry_release_code.get()
        localization = self.entry_release_localization.get().upper()
        quantity = self.entry_release_quantity.get()

        # Validation
        if not code or not localization or not quantity:
            self.show_message('release', 'Fill all fields', 'red')
            return

        if len(code) != 4 or not code.isdigit():
            self.show_message('release', 'Code must be 4 digits', 'red')
            self.clear_release_entries()
            return

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            self.show_message('release', 'Quantity must be positive number', 'red')
            self.clear_release_entries()
            return

        # API call
        data = {
            'code': code,
            'localization': localization,
            'quantity': quantity
        }

        response = self.api_request('PATCH', 'release_components/', data)

        if response is None:
            self.show_message('release', 'Connection error', 'red')
            return

        if response.status_code == 200:
            result = response.json()
            self.show_message('release', result.get('message', 'Released successfully'), 'blue')
        else:
            try:
                error = response.json()
                if 'message' in error:
                    self.show_message('release', error['message'], 'red')
                else:
                    error_msg = self.format_error(error)
                    self.show_message('release', error_msg, 'red')
            except:
                self.show_message('release', f'Error: {response.status_code}', 'red')

        self.clear_release_entries()

    def show_component_locations(self):
        """Show where component is located"""
        code = self.entry_show_code.get()

        if not code:
            self.show_message('show_component', 'Enter component code', 'red')
            return

        if len(code) != 4 or not code.isdigit():
            self.show_message('show_component', 'Code must be 4 digits', 'red')
            self.entry_show_code.delete(0, 'end')
            return

        # API call
        response = self.api_request('GET', f'component/{code}/localizations/')

        if response is None:
            self.show_message('show_component', 'Connection error', 'red')
            return

        if response.status_code == 200:
            result = response.json()

            if 'data' in result and result['data']:
                # Format output
                lines = [f"{'Localization':<15} {'Code':<8} {'Qty':<5}"]
                lines.append('-' * 35)
                for item in result['data']:
                    loc = item['localizations']
                    code = item['code']
                    qty = item['quantity']
                    lines.append(f"{loc:<15} {code:<8} {qty:<5}")

                text = '\n'.join(lines)
                self.show_message('show_component', text, 'blue')
            else:
                msg = result.get('message', f'Code {code} not found')
                self.show_message('show_component', msg, 'red')
        else:
            self.show_message('show_component', f'Error: {response.status_code}', 'red')

        self.entry_show_code.delete(0, 'end')

    def show_localization_contents(self):
        """Show what's in a localization"""
        localization = self.entry_show_localization.get().upper()

        if not localization:
            self.show_message('show_localization', 'Enter localization name', 'red')
            return

        # API call
        response = self.api_request('GET', f'localization/{localization}/components/')

        if response is None:
            self.show_message('show_localization', 'Connection error', 'red')
            return

        if response.status_code == 200:
            result = response.json()

            if 'data' in result and result['data']:
                # Format output
                loc_name = result.get('Localization', localization)
                lines = [f"Localization: {loc_name}", "=" * 35]
                lines.append(f"{'Code':<8} {'Quantity':<10}")
                lines.append('-' * 35)
                for item in result['data']:
                    code = item['code']
                    qty = item['quantity']
                    lines.append(f"{code:<8} {qty:<10}")

                text = '\n'.join(lines)
                self.show_message('show_localization', text, 'blue')
            else:
                msg = result.get('message', f'Localization {localization} is empty')
                self.show_message('show_localization', msg, 'red')
        elif response.status_code == 404:
            self.show_message('show_localization', f'Localization {localization} not found', 'red')
        else:
            self.show_message('show_localization', f'Error: {response.status_code}', 'red')

        self.entry_show_localization.delete(0, 'end')

    def clear_warehouse(self):
        """Admin: clear entire warehouse"""
        response = self.api_request('DELETE', 'clear_warehouse/')

        if response is None:
            self.label_admin_message.config(text='Connection error', fg='red')
            return

        if response.status_code == 200:
            result = response.json()
            msg = result.get('message', 'Warehouse cleared successfully')
            self.label_admin_message.config(text=msg, fg='green')
        else:
            self.label_admin_message.config(text=f'Error: {response.status_code}', fg='red')

    # ========== HELPER METHODS ==========

    def format_error(self, error_dict):
        """Format Django validation errors"""
        messages = []
        for field, errors in error_dict.items():
            if isinstance(errors, list):
                messages.extend(errors)
            else:
                messages.append(str(errors))
        return '\n'.join(messages)

    def show_message(self, frame_type, message, color):
        """Display message in appropriate frame"""
        if frame_type == 'login':
            label = self.label_login_error
        elif frame_type == 'add':
            label = self.label_add_message
        elif frame_type == 'release':
            label = self.label_release_message
        elif frame_type == 'show_component':
            label = self.label_show_component_message
        elif frame_type == 'show_localization':
            label = self.label_show_localization_message
        else:
            return

        current_text = label.cget('text')
        if current_text == message:
            label.config(text='', fg='black')
            label.after(100, lambda: label.config(text=message, fg=color))
        else:
            label.config(text=message, fg=color)

    def clear_add_entries(self):
        """Clear add frame entries"""
        self.entry_add_code.delete(0, 'end')
        self.entry_add_localization.delete(0, 'end')
        self.entry_add_quantity.delete(0, 'end')
        self.entry_add_code.focus_set()

    def clear_release_entries(self):
        """Clear release frame entries"""
        self.entry_release_code.delete(0, 'end')
        self.entry_release_localization.delete(0, 'end')
        self.entry_release_quantity.delete(0, 'end')
        self.entry_release_code.focus_set()

    # ========== FRAME NAVIGATION ==========

    def show_add_frame(self):
        """Show add component frame"""
        self.clear_add_entries()
        self.label_add_message.config(text='')
        self.frame_add.tkraise()
        self.entry_add_code.focus_set()
        self.current_frame = 'add'

    def show_release_frame(self):
        """Show release component frame"""
        self.clear_release_entries()
        self.label_release_message.config(text='')
        self.frame_release.tkraise()
        self.entry_release_code.focus_set()
        self.current_frame = 'release'

    def show_component_frame(self):
        """Show component locations frame"""
        self.entry_show_code.delete(0, 'end')
        self.label_show_component_message.config(text='')
        self.frame_show_component.tkraise()
        self.entry_show_code.focus_set()
        self.current_frame = 'show_component'

    def show_localization_frame(self):
        """Show localization contents frame"""
        self.entry_show_localization.delete(0, 'end')
        self.label_show_localization_message.config(text='')
        self.frame_show_localization.tkraise()
        self.entry_show_localization.focus_set()
        self.current_frame = 'show_localization'

    def go_back(self, event):
        """Navigate back (F3 key)"""
        if self.current_frame in ['add', 'release', 'show_component', 'show_localization']:
            # Clear current frame
            if self.current_frame == 'add':
                self.clear_add_entries()
                self.label_add_message.config(text='')
            elif self.current_frame == 'release':
                self.clear_release_entries()
                self.label_release_message.config(text='')
            elif self.current_frame == 'show_component':
                self.entry_show_code.delete(0, 'end')
                self.label_show_component_message.config(text='')
            elif self.current_frame == 'show_localization':
                self.entry_show_localization.delete(0, 'end')
                self.label_show_localization_message.config(text='')

            # Go back to logged in frame
            self.frame_logged_in.tkraise()
            self.current_frame = 'logged_in'

        elif self.current_frame == 'logged_in':
            # Logout
            self.auth = None
            self.is_admin = False
            self.label_login_error.config(text='')
            self.frame_login.tkraise()
            self.entry_login.focus_set()
            self.current_frame = 'login'

        elif self.current_frame == 'admin':
            # Admin logout
            self.auth = None
            self.is_admin = False
            self.label_admin_message.config(text='')
            self.frame_login.tkraise()
            self.entry_login.focus_set()
            self.current_frame = 'login'






    def handle_backspace(self, event):
        """Handle backspace navigation between fields"""
        widget = event.widget

        # Login frame
        if widget == self.entry_password and self.entry_password.get() == '':
            self.entry_login.focus_set()

        # Add frame
        if widget == self.entry_add_localization and self.entry_add_localization.get() == '':
            self.entry_add_code.focus_set()
        if widget == self.entry_add_quantity and self.entry_add_quantity.get() == '':
            self.entry_add_localization.focus_set()

        # Release frame
        if widget == self.entry_release_localization and self.entry_release_localization.get() == '':
            self.entry_release_code.focus_set()
        if widget == self.entry_release_quantity and self.entry_release_quantity.get() == '':
            self.entry_release_localization.focus_set()

        # ========== KEY BINDINGS ==========

    def setup_bindings(self):
        """Setup all keyboard bindings"""
        # Login frame
        self.entry_login.bind('<Return>', lambda e: self.entry_password.focus_set())
        self.entry_password.bind('<Return>', self.login_user)
        self.entry_password.bind('<BackSpace>', self.handle_backspace)

        # Add frame
        self.entry_add_code.bind('<Return>', lambda e: self.entry_add_localization.focus_set())
        self.entry_add_localization.bind('<Return>', lambda e: self.entry_add_quantity.focus_set())
        self.entry_add_localization.bind('<BackSpace>', self.handle_backspace)
        self.entry_add_quantity.bind('<Return>', lambda e: self.add_component())
        self.entry_add_quantity.bind('<BackSpace>', self.handle_backspace)

        # Release frame
        self.entry_release_code.bind('<Return>', lambda e: self.entry_release_localization.focus_set())
        self.entry_release_localization.bind('<Return>', lambda e: self.entry_release_quantity.focus_set())
        self.entry_release_localization.bind('<BackSpace>', self.handle_backspace)
        self.entry_release_quantity.bind('<Return>', lambda e: self.release_component())
        self.entry_release_quantity.bind('<BackSpace>', self.handle_backspace)

        # Show component frame
        self.entry_show_code.bind('<Return>', lambda e: self.show_component_locations())

        # Show localization frame
        self.entry_show_localization.bind('<Return>', lambda e: self.show_localization_contents())

        # Global bindings
        self.bind('<F3>', self.go_back)

        # Helper method for coordinates (development only)
        self.bind("<Button-1>", self.show_coordinates)
        self.show_coords = False  # Set to True to enable coordinate display

    def show_coordinates(self, event):
        """Helper method to show mouse coordinates (for development)"""
        if self.show_coords:
            print(f'x={event.x}, y={event.y}')

# Run application
if __name__ == '__main__':
    app = GUI()
    app.mainloop()