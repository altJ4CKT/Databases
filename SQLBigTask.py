import sqlite3

db = sqlite3.connect("./Imazon.db")
db.execute("CREATE TABLE IF NOT EXISTS Products ("
           "ProductID TEXT PRIMARY KEY, "
           "PName TEXT, "
           "Description TEXT, "
           "Price INTEGER )")

db.execute("CREATE TABLE IF NOT EXISTS Customer("
           "Customer_Id TEXT PRIMARY KEY, "
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
            tempDb.execute("INSERT INTO Customer(Customer_Id, Username, Password, Email, Contact_Number) VALUES(?,?,?,?,?)",
                            values)

        elif tableName == "Basket":
            data = tempDb.execute("SELECT Quantity FROM Basket "
                              "WHERE ProductID = ? "
                              "AND Customer_Id = ?", [1, 1])
            result = data.fetchall()

            if len(result) == 1:
                tempDb.execute("UPDATE Basket SET Quantity = ? "
                               "WHERE ProductID = ? "
                               "AND Customer_Id = ?", [result[0] + 1, 1, 1])
            else:
                tempDb.execute("INSERT INTO Basket(ProductID, Customer_Id) VALUES(?,?)",
                               values)
        tempDb.commit()
        tempDb.close()

    def getUniqueCustomers(self):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT Customer_Id FROM Customer")
        cIds = data.fetchall()
        print(cIds)

    def getUniqueProducts(self):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT ProductID FROM Products")
        pIds = data.fetchall()
        print(pIds)



db1: Database = Database("./Imazon.db")

print(db1.getUniqueCustomers())
print(db1.getUniqueProducts())

db1.insertIntoTable("Customer", ["C1", "JackT123", "ABC123", "JackT@gmail.com", 7947674954])





