import sqlite3


def printTwoDimArray(twoDimArray):
    for line in twoDimArray:
        for item in line:
            print(str(item), end=", ")
        print()


class Database:

    databaseRef: str

    def __init__(self, givenDatabaseRef: str):
        self.databaseRef = givenDatabaseRef

    def readAll(self, tableName: str):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT * "
                          "FROM " + tableName)
        result = data.fetchall()
        db.close()
        return result

    def printAll(self, tableName: str):
        printTwoDimArray(self.readAll(tableName))

    def createTable(self, tableName: str, tableFields: list[str]):
        db = sqlite3.connect(self.databaseRef)
        db.execute("CREATE TABLE " + tableName + " (" + ", ".join(tableFields) + ")")
        db.commit()
        db.close()


class DatabaseLikedSongs(Database):

    def __init__(self, givenDatabaseRef: str):
        super().__init__(givenDatabaseRef)

    def readTracksByArtist(self, givenArtist: str):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT * "
                          "FROM Tracks "
                          "WHERE Artist_Name = ?",
                          [givenArtist])
        result = data.fetchall()
        db.close()
        return result

    def printTracksByArtist(self, givenArtist: str):
        printTwoDimArray(self.readTracksByArtist(givenArtist))




db1: DatabaseLikedSongs = DatabaseLikedSongs("./Liked Songs.db")
print(db1.printTracksByArtist("Panic! At The Disco"))
 