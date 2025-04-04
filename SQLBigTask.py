import sqlite3
import  random
import tkinter as tk

db = sqlite3.connect("./Imazon.db")

db.execute("PRAGMA foreign_keys = ON")

db.execute("CREATE TABLE IF NOT EXISTS Products ("
           "ProductID TEXT PRIMARY KEY, "
           "PName TEXT, "
           "Description TEXT, "
           "Price INTEGER )")

db.execute("CREATE TABLE IF NOT EXISTS Customer("
           "Customer_Id INTEGER PRIMARY KEY AUTOINCREMENT, "
           "Username TEXT, "
           "Password TEXT, "
           "Email TEXT, "
           "Contact_Number INTEGER)")

db.execute("CREATE TABLE IF NOT EXISTS Basket("
           "ProductID TEXT, "
           "Customer_Id TEXT, "
           "Quantity INTEGER, "
           "FOREIGN KEY(ProductID) REFERENCES Products(ProductID), "
           "FOREIGN KEY(Customer_Id) REFERENCES Customer(Customer_Id), "
           "PRIMARY KEY(ProductID, Customer_Id)"
           ")")

db.commit()
db.close()

class Database:

    databaseRef: str

    def __init__(self, givenDatabaseRef: str):

        self.databaseRef = givenDatabaseRef

    def insertIntoTable(self, tableName, values: list):

        tempDb = sqlite3.connect(self.databaseRef)

        if tableName == "Products":
            tempDb.execute("INSERT INTO Products(ProductID, PName, Description, Price) VALUES(?,?,?,?)",
                            values)

        elif tableName == "Customer":
            tempDb.execute("INSERT INTO Customer(Username, Password, Email, Contact_Number) VALUES(?,?,?,?)",
                            values)

        elif tableName == "Basket":
            try:
                tempDb.execute("INSERT INTO Basket(ProductID, Customer_Id, Quantity) VALUES(?,?,?)",
                               values)

            except sqlite3.IntegrityError:
                quantity = tempDb.execute("SELECT Quantity FROM Basket "
                                          "WHERE ProductID = ?"
                                          "AND Customer_Id = ?", [values[0], values[1]])
                quantity = quantity.fetchone()[0]
                quantity += 1
                tempDb.execute("UPDATE Basket SET Quantity = ? "
                           "WHERE ProductID = ?"
                           "AND Customer_Id = ?", [quantity, values[0], values[1]])



        tempDb.commit()
        tempDb.close()

    def getUniqueCustomers(self):

        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT DISTINCT Customer_Id FROM Customer")
        cIds = data.fetchall()
        print(cIds)

    def getUniqueProducts(self):

        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT DISTINCT ProductID FROM Products")
        pIds = data.fetchall()
        print(pIds)

class RegisterFrame(tk.Frame):
    usernameEntry: tk.Entry
    passwordEntry: tk.Entry
    emailEntry: tk.Entry
    phoneEntry: tk.Entry

    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame):

        if oldFrame is not None:
            oldFrame.destroy()

        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):
        self.configure(bg="#000000")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        tk.Button(self, text="Cancel", command=lambda: LoginRegisterFrame(self.master, self),
                  font=["Century Gothic", 20],
                  width=10).grid(row=5, column=0)
        tk.Button(self, text="Submit", command=lambda: self.submitButtonClicked(),
                  font=["Century Gothic", 20],
                  width=10).grid(row=5, column=4)

        tk.Label(self, text="Username", font=("Century Gothic", 20), width=10).grid(row=0, column=1)
        self.usernameEntry = tk.Entry(self, font=("Century Gothic", 20), width=30)
        self.usernameEntry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self, text="Password", font=("Century Gothic", 20), width=10).grid(row=1, column=1)
        self.passwordEntry = tk.Entry(self, font=("Century Gothic", 20), width=30)
        self.passwordEntry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self, text="Email", font=("Century Gothic", 20), width=10).grid(row=2, column=1)
        self.emailEntry = tk.Entry(self, font=("Century Gothic", 20), width=30)
        self.emailEntry.grid(row=2, column=3, padx=5, pady=5)

        tk.Label(self, text="Phone", font=("Century Gothic", 20), width=10).grid(row=3, column=1)
        self.phoneEntry = tk.Entry(self, font=("Century Gothic", 20), width=30)
        self.phoneEntry.grid(row=3, column=3, padx=5, pady=5)

    def submitButtonClicked(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        email = self.emailEntry.get()
        phone = self.phoneEntry.get()

        db1.insertIntoTable("Customer", [username, password, email, phone])

        tempDb = sqlite3.connect("./Imazon.db")

        cId = tempDb.execute("SELECT Customer_Id FROM Customer "
                              "WHERE Username = ?"
                              "AND Password = ?",
                              [username, password])

        cId = cId.fetchone()[0]

        print(f"Your Customer ID is {cId}")

        tempDb.commit()
        tempDb.close()


class LoginFrame(tk.Frame):
    usernameEntry: tk.Entry
    passwordEntry: tk.Entry

    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame):

        if oldFrame is not None:
            oldFrame.destroy()

        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):
        self.configure(bg="#000000")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        tk.Button(self, text="Cancel", command=lambda: LoginRegisterFrame(self.master, self),
                 font=["Century Gothic", 20],
                 width=10).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self, text="Submit", command=lambda: self.submitButtonClicked(),
                  font=["Century Gothic", 20],
                  width=10).grid(row=3, column=4, padx=5, pady=5)

        tk.Label(self, text="Username", font=("Century Gothic", 20), width=10).grid(row=1, column=1)
        self.usernameEntry = tk.Entry(self, font=("Century Gothic", 20), width=30)
        self.usernameEntry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self, text="Password", font=("Century Gothic", 20), width=10).grid(row=2, column=1)
        self.passwordEntry = tk.Entry(self, font=("Century Gothic", 20), width=30)
        self.passwordEntry.grid(row=2, column=3, padx=5, pady=5)

    def submitButtonClicked(self):

        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        print(f"username: {username}, password: {password}")

class LoginRegisterFrame(tk.Frame):
    def __init__(self, windowRef: tk.Tk, oldFrame: tk.Frame):

        if oldFrame is not None:
            oldFrame.destroy()

        super().__init__(windowRef)
        self.SetupLayout()
        self.pack(fill="both", expand=True)

    def SetupLayout(self):
        self.configure(bg="#FF00FF")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        tk.Button(self, text="Login", command=lambda: LoginFrame(self.master, self), font=["Century Gothic", 20],
                  width=10).grid(row=0, column=0, padx=(10, 5), pady=10)
        tk.Button(self, text="Register", command=lambda: RegisterFrame(self.master, self), font=["Century Gothic", 20],
                  width=10).grid(
            row=0, column=1, padx=(5, 10), pady=10)

class MainProgram(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Main Window")

        self.configure(bg="#ff8000")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        LoginRegisterFrame(self, None)
        self.mainloop()

db1: Database = Database("./Imazon.db")

x: MainProgram = MainProgram()









