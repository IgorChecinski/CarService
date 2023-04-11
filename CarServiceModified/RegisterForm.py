import tkinter as tk
import tkinter.messagebox


class RegisterForm: 
    def __init__(self):
        self.window = tk.Tk() 
        self.window.title("Registration form") 

        tk.Label(self.window, text="Login:").grid(row=0) 
        self.username = tk.Entry(self.window) 
        self.username.grid(row=0, column=1) 

        tk.Label(self.window, text="Email:").grid(row=1)
        self.email = tk.Entry(self.window)
        self.email.grid(row=1, column=1)

        tk.Label(self.window, text="Password:").grid(row=2)
        self.password = tk.Entry(self.window, show="*")
        self.password.grid(row=2, column=1)

        tk.Label(self.window, text="Repeat password:").grid(row=3)
        self.confirm_password = tk.Entry(self.window, show="*")
        self.confirm_password.grid(row=3, column=1)

        tk.Button(self.window, text="Register", command=self.submit).grid(row=4, column=0, columnspan=2, pady=10) 

        self.window.mainloop() 

    def submit(self):
        try: 
            username = self.username.get() 
            email = self.email.get()
            password = self.password.get()
            confirm_password = self.confirm_password.get()

            if "@" not in email: 
                raise Exception("Email does not contain \'@\'") 

            if password != confirm_password:
                raise Exception("provided passwords are different")

            if len(password) < 8:
                raise Exception("password to short")

            if not any(char.isdigit() for char in password):
                raise Exception("Hasło musi posiadać przynajmniej jedną cyfre")

            if not any(char.isupper() for char in password):
                raise Exception("password needs at least one big letter")

            if not any(char in "!@#$%^&*()_+-=[]{}|;':,.<>?/" for char in password):
                raise Exception("password needs at least one special character")
            open_for_check = open("data.txt", "r") 
            read_for_check = open_for_check.read() 
            if username not in read_for_check and email not in read_for_check: 
                with open("data.txt", "a") as file: 
                    file.write(f"{self.username.get()},{self.email.get()}\n")           
                tk.messagebox.showinfo("Info", "Registration successful!") 
                open_for_check.close() 
            else:  
                raise Exception("Given email is already used for a difrent account!")
        except Exception as error:  
            tk.messagebox.showerror("Error!", str(error))
RegisterForm() 