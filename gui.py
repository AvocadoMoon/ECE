from tkinter import *

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# TO DO FOR PASSWORD LABELS: show='*'
# !!!!!!!!!!!!!!!!!!!!!!

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()  # hide the chat window temporarily while we make the user log in
        self._login()

        self.connection = None
        
    def run(self):
        self.window.mainloop()

    def _login(self):
        self.login = Toplevel() # login window
        self.login.title = "Login"
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 400, height = 300, bg=BG_COLOR)

        # Label that tells user they are required to log in
        self.require = Label(self.login, text = "Login to continue", justify = CENTER, font = FONT_BOLD)
        self.require.place(relheight = 0.15, relx = 0.2, rely = 0.07)

        # username and password labels
        self.username = Label(self.login, text= "Username: ", font = "Helvetica 12")
        self.username.place(relheight = 0.2, relx = 0.1, rely = 0.2)
        self.password = Label(self.login, text= "Password: ", font = "Helvetica 12")
        self.password.place(relheight = 0.2, relx = 0.1, rely = 0.4)

        # entry boxes for typing username and password
        self.entry_username = Entry(self.login, font = "Helvetica 12")
        self.entry_username.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)

        self.entry_password = Entry(self.login, font = "Helvetica 12")
        self.entry_password.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.4)

        # failed login label
        self.fail = Label(self.login, text = "Login Failed", justify = CENTER, font = FONT_BOLD, fg="#d90202")

        # login button 
        self.attempt_login = Button(self.login, text="Login", font=FONT_BOLD, width=20, fg="#000000",
                             command=lambda: self._verify_credentials(self.entry_username.get(), self.entry_password.get()))
        self.attempt_login.place(x=150, y=200)

        # create new account button
        self.create_account = Button(self.login, text="Create a new account", font = "Helvetica 10", width=20, fg="#000000",
                             command=lambda: self._create_new_account()) 
        self.create_account.place(x=150, y=250)

    def _verify_credentials(self, entry_username, entry_password):
        # open the credentials file and parse it. this is inefficient. needs to be optimized/cleaned up...
        f = open('credentials.txt', 'r') # open the file
        credentials = f.readlines() # read all the lines

        for c in credentials:   # for each line in the file, split it at the colon
            info = c.split(':')
            username, password = info[0], info[1]   # extract the username and password 
            if entry_username == username:  # if we found the matching username...
                if entry_password == password.strip():
                    self.sender = entry_username  # create a new attribute for the sender's name
                    self.login.destroy() # successful login! so we can destroy the login window
                    self._setup_main_window()   # open the actual chat window
                else:
                    self.fail.forget() # initially hide the failure label so that it pops up new every time
                    self.fail.place(relheight = 0.15, relx = 0.45, rely = 0.75) # display that the login failed
                    break
            else:
                    self.fail.forget() # initially hide the failure label so that it pops up new every time
                    self.fail.place(relheight = 0.15, relx = 0.45, rely = 0.75) # display that the login failed
                    break

    def _create_new_account(self):
        self.account = Toplevel() # create new account window

        self.account.title = "Create a new account"
        self.account.resizable(width = False, height = False)
        self.account.configure(width = 400, height = 300)

        # Label that tells user they are here to create a new account
        self.new = Label(self.account, text = "Create a new account", justify = CENTER, font = FONT_BOLD)
        self.new.place(relheight = 0.15, relx = 0.2, rely = 0.07)

        # new username, password, and re-enter password labels
        self.new_username = Label(self.account, text= "Enter a username: ", font = "Helvetica 12")
        self.new_username.place(relheight = 0.2, relx = 0.1, rely = 0.2)
        self.new_password = Label(self.account, text= "Enter a password: ", font = "Helvetica 12")
        self.new_password.place(relheight = 0.2, relx = 0.1, rely = 0.6)
        
        # todo for future
        # self.reenter = Label(self.account, text= "Re-enter the same password: ", font = "Helvetica 12")
        # self.reenter.place(relheight = 0.2, relx = 0.1, rely = 1)

        # entry boxes for typing username and password
        self.entry_new_username = Entry(self.account, font = "Helvetica 12")
        self.entry_new_username.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)

        self.entry_new_password = Entry(self.account, font = "Helvetica 12")
        self.entry_new_password.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.6)

        # todo for future
        # self.entry_reenter = Entry(self.account, font = "Helvetica 12")
        # self.entry_reenter.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 1)

        self.create = Button(self.account, text="Create a new account", font = FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._store_credentials(self.entry_new_username.get(), self.entry_new_password.get())) 
        self.create.place(x=150, y=250)

    def _store_credentials(self, username, password):
        f = open('credentials.txt', 'a')
        f.write('\n')
        f.write(username + ':' + password)
        f.close()

        # allow user to close out of this window now
        self.account.after(2000) # delay for 2 seconds 
        self.new.forget()
        self.new_username.forget()
        self.new_password.forget()
        self.entry_new_username.forget()
        self.entry_new_password.forget()
        self.create.forget()

        self.success = Label(self.account, text = "Account successfully created! You may now close out of this window and proceed to the login.", justify = CENTER, font = FONT_BOLD)
        self.success.place(relheight = 0.15, relx = 0.2, rely = 0.07)



    def _setup_main_window(self):
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
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END) #clears message entry box
        msg1 = f"{sender}: {msg}\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1) #inserts message to widget
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
    
    def _recieveMessage(self, msg):
        self.msg_entry.delete(0, END)
        msg1 = f"{msg}\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()