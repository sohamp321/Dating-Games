from User import UserModel
import json


class Repo():
    def __init__(self, db) -> None:
        self.conn = db.conn
        self.cur = db.cur

    def createUserTable(self):
        try:
            query = """CREATE TABLE IF NOT EXISTS "User" (
                "index" SERIAL UNIQUE,
                "name" TEXT,
                "gender" TEXT, 
                "userid" TEXT PRIMARY KEY UNIQUE,
                "password" TEXT,
	            "avatar" SMALLINT,
	            "bio" TEXT,
	            "country" TEXT,
	            "DOB" TEXT,
                "partner" TEXT,
                "messages" TEXT
            );"""
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    def addUser(self, user):
        try:
            query = """INSERT INTO "User" ( "name" ,"gender","userid","password","avatar","bio","country","DOB","partner","messages") VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(
                user.name, user.gender, user.userid, user.password, user.avatar, user.bio, user.country, user.DOB, user.partner ,json.dumps(user.messages))
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserProfile(self, user):
        try:
            query = """UPDATE "User"
                    SET "name" = '{}',
                        "gender" = '{}',
                        "bio" = '{}',
                        "country" = '{}',
                        "DOB" = '{}',
                        "partner" = '{}'
                    WHERE "userid" = '{}';""".format(user.name,user.gender ,user.bio, user.country, user.DOB, user.partner ,user.userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserMessages(self,messages,userid):
        try:
            query = """UPDATE "User"
                    SET "messages" = '{}'
                    WHERE "userid" = '{}';""".format(json.dumps(messages), userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserPassword(self, password, userid):
        try:
            query = """UPDATE "User"
                    SET "password" = '{}'
                    WHERE "userid" = '{}';""".format(password, userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def isUserIdUsed(self, userid):
        try:
            query = """ SELECT * from "User" WHERE "userid" = '{}';""".format(
                userid)
            self.cur.execute(query)
            row = self.cur.fetchall()
        except Exception as e:
            print(e)
            return 1
        if(len(row)):
            return True
        else:
            return False

    def getUserById(self, userid):
        try:
            query = """ SELECT * from "User" WHERE "userid" = '{}';""".format(
                userid)
            self.cur.execute(query)
            userTable = self.cur.fetchall()
            user = UserModel.User(
                userTable[0][0], userTable[0][1], userTable[0][2], userTable[0][3], userTable[0][4], userTable[0][5], userTable[0][6], userTable[0][7], userTable[0][8],userTable[0][9], json.loads(userTable[0][10]))
        except Exception as e:
            print(e)
            return [False, None]
        return [True, user]

    def getUserByIndex(self, index):
        try:
            query = """ SELECT * from "User" WHERE "index" = '{}';""".format(
                index)
            self.cur.execute(query)
            userTable = self.cur.fetchall()
            user = UserModel.User(
                userTable[0][0], userTable[0][1], userTable[0][2], userTable[0][3], userTable[0][4], userTable[0][5], userTable[0][6], userTable[0][7], userTable[0][8],userTable[0][9], json.loads(userTable[0][10]))
        except Exception as e:
            print(e)
            return [False, None]
        return [True, user]

    def getAllUsers(self):
        try:
            query = """ SELECT * from "User"; """
            self.cur.execute(query)
            userTable = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        users = []
        for row in userTable:
            user = UserModel.User(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9], json.loads(row[10]))
            users.append(user)
        return [True, users]

    def getNumberOfUsers(self):
        try:
            query = """ SELECT * from "User"; """
            self.cur.execute(query)
            userTable = self.cur.fetchall()
        except Exception as e:
            print(e)
            return [False, None]
        return [True, len(userTable)]

    def deleteUserById(self, userid):
        try:
            query = """DELETE from "User" WHERE "userid" = '{}';""".format(
                userid)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def deleteUserByIndex(self, index):
        try:
            query = """DELETE from "User" WHERE "index" = '{}';""".format(
                index)
            self.cur.execute(query)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def delteUserTable(self):
        try:
            query = """ DROP TABLE IF EXISTS "User"; """
            self.cur.execute(query)
        except Exception as e:
            print(e)
            return False
        return True