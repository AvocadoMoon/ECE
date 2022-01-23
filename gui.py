import threading
from tkinter import *
import protocol
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfile  # allows us to upload an image
from PIL import ImageTk, Image
from Crypto.Hash import SHA256  # pip install pycryptodome

# https://ttkbootstrap.readthedocs.io/en/latest/gettingstarted/installation/ 
# install with pip 

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
ACTIVE_COLOR = "#17202F"
CHECKBUTTON_COLOR = "#000000"
WHITE = "#FFFFFF"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# TO DO FOR PASSWORD LABELS: show='*'
# !!!!!!!!!!!!!!!!!!!!!!

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()  # hide the chat window temporarily while we make the user log in
        self._login()
        self.username = None

        self.connection = None
        self.send_image = False
        self.files = []

        
    def run(self):
        self.window.mainloop()

    def _login(self):
        self.login = Toplevel() # login window
        self.login.title = "Login"
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 400, height = 300)

        # Label that tells user they are required to log in
        self.require = ttk.Label(self.login, text = "Login to continue", bootstyle="default")
        self.require.place(relheight = 0.15, relx = 0.4, rely = 0.07)

        # username and password labels
        usernameLabel = ttk.Label(self.login, text= "Username: ", bootstyle="default")
        usernameLabel.place(relheight = 0.2, relx = 0.1, rely = 0.2)
        passwordLabel = ttk.Label(self.login, text= "Password: ", bootstyle="default")
        passwordLabel.place(relheight = 0.2, relx = 0.1, rely = 0.4)

        # entry boxes for typing username and password
        self.entry_username = ttk.Entry(self.login, bootstyle="primary")
        self.entry_username.place(relwidth = 0.4, relheight = 0.12, relx = 0.30, rely = 0.25)
        self.entry_username.focus()
        self.entry_password = ttk.Entry(self.login, bootstyle="primary", show="*")
        self.entry_password.place(relwidth = 0.4, relheight = 0.12, relx = 0.30, rely = 0.45)
        # login if user presses enter/return
        self.entry_password.bind("<Return>", lambda event: self._verify_credentials(self.entry_username.get(), self.entry_password.get()))

        # failed login label
        self.fail = ttk.Label(self.login, text = "Login Failed", justify = CENTER, bootstyle="danger")

        # login button 
        self.attempt_login = ttk.Button(self.login, text="Login", width=20, bootstyle="default",
                             command=lambda: self._verify_credentials(self.entry_username.get(), self.entry_password.get()))
        self.attempt_login.place(x=110, y=210)

        # create new account button
        self.create_account = ttk.Button(self.login, text="Create a new account", width=20, bootstyle="default-outline",
                             command=lambda: self._create_new_account()) 
        self.create_account.place(x=110, y=250)



    def _verify_credentials(self, entry_username, entry_password):
        # open the credentials file and parse it. this is inefficient. needs to be optimized/cleaned up...
        f = open('credentials.txt', 'r') # open the file
        credentials = f.readlines() # read all the lines

        for c in credentials:   # for each line in the file, split it at the colon
            info = c.split(':')
            username, password = info[0], info[1]   # extract the username and password 
            print(entry_username, entry_password)
            #print('credentials:', username, password)
            obj = SHA256.new(data=entry_password.encode())
            hashed_password = obj.digest()
            if entry_username == username and str(hashed_password) == password.strip():
                self.username = username    # get their username
                self.sender = entry_username  # create a new attribute for the sender's name
                self.login.destroy() # successful login! so we can destroy the login window
                self._connect() #now let the user decide which server its going to join or if its going to be the server
                # self._setup_main_window()   # open the actual chat window
                # should be commented ^^^
        self.fail.place(relheight = 0.08, x = 160, y = 175) # if credentials were incorrect, tell the user that the login failed
                
    
    #still need to add login button
    def _connect(self):
        
        def connection():
            self.server = True
            if self.serverVar.get() == 0:
                self.server = False
            self.connection = protocol.Connection(int(port.get()), ip.get(), self.username, self.server, self)
            self.connection.connect()
            self._setup_main_window()


        self.connectWindow = Toplevel(self.window)

        self.connectWindow.title("Set Connection Settings")
        self.connectWindow.resizable(width=False, height=False)
        self.connectWindow.configure(width=400, height=400, bg=WHITE)

        self.serverVar = IntVar()
        serverButton = Checkbutton(self.connectWindow, text="Hosting Server", onvalue=1, offvalue=0, height=2, width=10, bg=BG_COLOR, fg=TEXT_COLOR, activebackground=BG_COLOR, 
        activeforeground=TEXT_COLOR,selectcolor=CHECKBUTTON_COLOR, relief=FLAT, variable=self.serverVar)

        serverButton.place(relheight=0.07, relx=0.35, rely=0.8, relwidth=0.35)

        ip_label = Label(self.connectWindow, text="Enter IP: ", font=FONT, height=5, width=10, background=BG_COLOR, fg= TEXT_COLOR)
        ip = Entry(self.connectWindow, font=FONT, background=BG_COLOR, foreground=TEXT_COLOR)
        ip_label.place(relheight=0.2, relx=0.1, rely=0.07)
        ip.place(relheight=0.1, relx=0.4, rely=0.11)

        port_label = Label(self.connectWindow, text="Enter Port: ", font=FONT, height=5, width=10, background=BG_COLOR, fg= TEXT_COLOR)
        port = Entry(self.connectWindow, font=FONT, background=BG_COLOR, foreground=TEXT_COLOR)
        port_label.place(relheight=0.2, relx=0.1, rely=0.2)
        port.place(relheight=0.1, relx=0.4, rely=0.241)

        password_label = Label(self.connectWindow, text="Enter Server \n Password: ", font=FONT, height=3, width=12, background=BG_COLOR, fg= TEXT_COLOR, wraplength=150)
        password = Entry(self.connectWindow, font=FONT, background=BG_COLOR, foreground=TEXT_COLOR)
        password_label.place(relheight=0.15, relx=0.1, rely=0.341)
        password.place(relheight=0.1, relx=0.4, rely=0.372)


        connectButton = Button(self.connectWindow, text="Connect", width=20, command=connection, bg=BG_COLOR, fg=TEXT_COLOR)
        connectButton.place(relheight=0.1, relx=0.4, rely=0.65, relwidth=0.15)
        


    def _create_new_account(self):
        self.account = Toplevel() # create new account window

        self.account.title("Create a new account")
        self.account.resizable(width = False, height = False)
        self.account.configure(width = 400, height = 300)

        # Label that tells user they are here to create a new account
        self.new = ttk.Label(self.account, text = "Create a new account", justify = CENTER, style="default")
        self.new.place(relheight = 0.15, relx = 0.35, rely = 0.07)

        # new username, password, and re-enter password labels
        self.new_username = ttk.Label(self.account, text= "Enter a username: ", style="default")
        self.new_username.place(relheight = 0.2, relx = 0.1, rely = 0.2)
        self.new_password = ttk.Label(self.account, text= "Enter a password: ", style="default")
        self.new_password.place(relheight = 0.2, relx = 0.1, rely = 0.4)
        
        # todo for future
        # self.reenter = Label(self.account, text= "Re-enter the same password: ", font = "Helvetica 12")
        # self.reenter.place(relheight = 0.2, relx = 0.1, rely = 1)

        # entry boxes for typing username and password
        self.entry_new_username = ttk.Entry(self.account, style="success")
        self.entry_new_username.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.25)

        self.entry_new_password = ttk.Entry(self.account, style="success", show="*")
        self.entry_new_password.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.45)

        # todo for future
        # self.entry_reenter = Entry(self.account, font = "Helvetica 12")
        # self.entry_reenter.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 1)

        self.create = ttk.Button(self.account, text="Create a new account", width=20, style="success-outline",
                             command=lambda: self._store_credentials(self.entry_new_username.get(), self.entry_new_password.get())) 
        self.create.place(x=110, y=190)

    def _store_credentials(self, username, password):
        if not(username) or not(password):
            self.please = ttk.Label(self.account, text = "Please enter a username and password", justify = CENTER, bootstyle="danger")
            self.please.place(relheight = 0.15, relx = 0.2, rely = .8)
        else:
            f = open('credentials.txt', 'a')
            f.write('\n')
            obj = SHA256.new(data = password.encode())
            hashed_password = obj.digest()
            f.write(username + ':' + str(hashed_password))
            f.close()

            # allow user to close out of this window now
            self.account.after(2000) # delay for 2 seconds 
            try:
                self.please.destroy()
            except:
                self.new.destroy()
                self.new_username.destroy()
                self.new_password.destroy()
                self.entry_new_username.destroy()
                self.entry_new_password.destroy()
                self.create.destroy()

            self.success = ttk.Label(self.account, text = "Account successfully created! \nYou may now close out of this window and proceed to the login.", justify = CENTER, bootstyle="success")
            self.success.place(relheight = 0.15, relx = 0.02, rely = 0.4)

    def _setup_main_window(self):
        self.connectWindow.destroy()
        self.window.deiconify() # show the chat window
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Message Center", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # bottom label
        self.bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        self.bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(self.bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # send button
        send_button = Button(self.bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(self.send_image))
        send_button.place(relx=0.77, rely=0.008, relheight=0.02, relwidth=0.22)

         # upload file button
        upload_file = Button(self.bottom_label, text="Upload File", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._open_file())
        upload_file.place(relx=0.77, rely=0.040, relheight=0.02, relwidth=0.22)

        # logout button
        logout_button = ttk.Button(self.window, text="Logout", bootstyle="primary", command=lambda: self._on_logout_pressed()) 
        logout_button.place(x=380, y=10)

    def _open_file(self):
        self.path = askopenfile(mode='r', filetypes=[('Image', '*.png *.jpg *.jpeg')]) # get image path
        if self.path:   # if the user actually chose an image (aka didn't close out of the window)
            img = Image.open(self.path.name)
            img = img.resize((img.width // 2, img.height // 2)) # shrink the image arbitrarily... need to standardize this somehow.
            self.image = ImageTk.PhotoImage(img) # create a Tkinter PhotoImage object
            self.files.append(self.image)

            # pseudo display for the image (so that we can scroll)
            self.img_entry = Text(self.bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
            self.img_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

            # scrollbar
            msg_scrollbar = Scrollbar(self.img_entry)
            msg_scrollbar.place(relheight=1, relx=0.974)
            msg_scrollbar.configure(command=self.img_entry.yview)

            # insert the image
            self.img_entry.image_create(END, image=self.files[-1])

            # boolean flag to indicate whether or not we're sending an image
            self.send_image = True

            # allow us to press enter to send
            self.img_entry.focus()  # this isn't working??
            self.img_entry.bind('<Return>', lambda event: self._on_enter_pressed(self.send_image))
        return

     
    def _on_logout_pressed(self):
        self.window.withdraw()
        self.__init__()

    def _on_enter_pressed(self, event):
        if self.send_image: # if we are sending an image...
            msg = self.path
            msg1 = f"You: "
            self.img_entry.destroy()
        else:
            msg = self.msg_entry.get()
            if not msg:
                return
            msg1 = f"You: {msg}\n"

        # self.connection.sendMessage(msg)  # NEED TO UPDATE THIS FUNCTION TO SUPPORT IMAGES!!! TODO
        # potential idea: if sending an image... call sendImage(). if sending a text message... call sendMessage()
        # that should work ^ because separate functions will handle the differences between sending images vs text messages
        self.msg_entry.delete(0, END) #clears message entry box
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1) #inserts message to widget

        if self.send_image:
            self.text_widget.image_create(END, image=self.files[-1])
            self.text_widget.insert(END, '\n')
            self.send_image = False # reset this flag to be false. might need to relocate this

        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
    
    def displayRecievedMessages(self, msg): # TODO: add support for receiving an image. 
        msg1 = f"{msg}\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()