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

    def createTable(self, tableName: str, tableFields: list[str]) -> None:
        db = sqlite3.connect(self.databaseRef)
        db.execute("CREATE TABLE " + tableName + " (" + ", ".join(tableFields) + ")")
        db.commit()
        db.close()
    
    def createTableIfNotExists(self, tableName: str, tableFields: list[str]) -> None:
        db = sqlite3.connect(self.databaseRef)
        db.execute("CREATE TABLE IF NOT EXISTS " + tableName + " (" + ", ".join(tableFields) + ")")
        db.commit()
        db.close()

    def insertIntoTable(self, tableName: str, data: list[any]) -> bool:
        db = sqlite3.connect(self.databaseRef)
        db.execute("INSERT INTO " + tableName + " VALUES (" + ", ".join(["?" for _ in data]) + ")", data)
        db.commit()
        db.close()
        return True


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

    def addNewTrack(self, trackName: str, artistName: str, albumName: str, albumArtistName: str, trackNumber: int, trackDuration: int, explicit: bool, trackPreviewURL: str = None) -> bool:
        return self.insertIntoTable("Tracks", [trackName, artistName, albumName, albumArtistName, trackNumber, trackDuration, explicit, trackPreviewURL])

    def addNewAlbum(self, albumName: str, albumArtistName: str, albumArtUrl: str, albumReleaseDate: str) -> bool:
        return self.insertIntoTable("Albums", [albumName, albumArtistName, albumArtUrl, albumReleaseDate])


db1: DatabaseLikedSongs = DatabaseLikedSongs("./Liked Songs.db")
print(db1.printTracksByArtist("Panic! At The Disco"))
 