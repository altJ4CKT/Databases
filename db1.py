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

    def createTable(self, tableName: str, tableFields: list[str]) -> bool:
        try:
            dbC = sqlite3.connect("./" + tableName + ".db")
            dbC.execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({', '.join(tableFields)})")
            dbC.close()
            return True
        except sqlite3.OperationalError as e:
            print(f"An error occurred: {e}")
            return False


    def updateRecords(self, tableName: str, whatField: dict[str:any], whereField: dict[str:any]):
        qStr = "UPDATE " + tableName + " SET"
        qStr += list(whatField.keys())[0] + " = ? WHERE "
        for i in range(len(whereField)):
            qStr += list(whereField.keys())[i] + " = ? "
            if i != len(whereField) - 1:
                qStr += " AND "
        db = sqlite3.connect(self.databaseRef)
        db.execute(qStr, list(whatField.values()) + list(whereField.values()))
        db.commit()
        db.close()



class DatabaseLikedSongs(Database):

    def __init__(self, givenDatabaseRef: str):
        super().__init__(givenDatabaseRef)

    def readTracksByArtist(self, givenArtist: str):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT DISTINCT Artist_Name "
                        "FROM Tracks "
                        "WHERE Artist_Name LIKE ? ",
                        [givenArtist])
        result = data.fetchall()
        db.close()
        return result

    def printTracksByArtist(self, givenArtist: str):
        printTwoDimArray(self.readTracksByArtist(givenArtist))

    def getRowIds(self):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT rowid, Track_Name "
                          "FROM Tracks ")
        result = data.fetchall()
        db.close()
        return result

    def updateExplicit(self, trackName: str, trackArtist: str, explicit: int):
        db = sqlite3.connect(self.databaseRef)
        db.execute("UPDATE Tracks "
                    "SET Explicit = ? "
                    "WHERE Track_Name = ? "
                    "AND Artist_Name = ? ",
                    [explicit, trackName, trackArtist])
        db.commit()
        db.close()

    def deleteAllByArtist(self, artistName: str):
        db = sqlite3.connect(self.databaseRef)
        db.execute("DELETE FROM Tracks "
                   "WHERE Artist_Name = ? ",
                    [artistName])
        db.commit()
        db.close()

    def readTracksLongerThanDuration(self, duration: int):
        durationMS: int = duration*60*1000
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT Track_Name, Artist_Name, Track_Duration "
                          "FROM Tracks "
                          "WHERE Track_Duration > ? ",
                          [durationMS])
        result = data.fetchall()
        db.close()
        return result

    def artistSearch(self, character):
        db = sqlite3.connect(self.databaseRef)
        data = db.execute("SELECT Artist_Name "
                          "FROM Tracks "
                          "WHERE Artist_Name LIKE ?",
                          [f"%{character}%"])

db1: DatabaseLikedSongs = DatabaseLikedSongs("./Liked Songs.db")
print(db1.readTracksLongerThanDuration(8))
# print(db1.readTracksByArtist("%Calvin Harris"))
# db1.printTracksByArtist("GAYLE")
# db1.updateRecords("Tracks", {"Explicit": 0}, {"Artist_Name": "GAYLE", "Track_Name": "abcdefu"})
# db1.printTracksByArtist("GAYLE")
# db1.dropTable("Tracks")
# db1.deleteAllByArtist("Eminem")
# db1.printTracksByArtist("Eminem")
# print(db1.printTracksByArtist("Panic! At The Disco"))
# db1.insertIntoTable("Tracks",["Test","1234","Test","1234","Test","1234","Test","1234",])
# print(db1.readTracksLongerThanDuration(7))





