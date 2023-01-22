from flask import session
from User import UserRepo
import bcrypt
from datetime import date


class UserServices:

    def __init__(self, db) -> None:
        self.db = UserRepo.Repo(db)

    def login(self, user):
        if('@' not in user.userid or len(user.userid) < 3):
            return [False, "Invalid Email"]
        if(len(user.password) < 6):
            return [False, "Incorrect Username or Password"]
        userData = self.db.getUserById(user.userid)
        if (userData[0]):
            if (bcrypt.checkpw(str(user.password).encode('utf-8'), str(userData[1].password).encode('utf-8'))):
                return userData
            else:
                return [False, "Incorrect Username or Password"]
        else:
            return [False, "User Does Not Exists, try signing up"]

    def register(self, user):
        if (self.db.isUserIdUsed(user.userid)):
            print("user id already used")
            return [False, "Email already registered"]

        hashed = bcrypt.hashpw(
            str(user.password).encode('utf-8'), bcrypt.gensalt())
        user.password = hashed.decode()
        if (self.db.addUser(user)):
            print("user added successfully")
            return [True, "Added User Successfully"]
        else:
            return [False, "Database Error"]

    def validateData(self, name, email, password, confirmpassword, DOB, country, gender):
        if(name == "" or email == "" or password == "" or confirmpassword == "" or DOB == "" or country == "" or gender == ""):
            return [False, "Please Fill all the Fields"]
        if(" " not in name):
            return [False, "Please Enter Full Name"]
        if('@' not in email or len(email) < 3):
            return [False, "Invalid Email Address"]
        if(password != confirmpassword):
            return [False, "Confirm password did not match"]
        if(len(password) < 6):
            return [False, "Password should consist of atleast 6 characters"]
        return [True, "Valid Data"]

    def signout(self):
        print("signing out")
        session.pop("index", None)

    def getUserSession(self, index):
        userData = self.db.getUserByIndex(index)
        if (userData[0]):
            print("session retrived successfully")
        else:
            self.signout()
        return userData

    def editProfile(self, user):
        userData = self.db.getUserById(user.userid)
        if(userData[0]):
            if (bcrypt.checkpw(str(user.password).encode('utf-8'), str(userData[1].password).encode('utf-8'))):
                user.password = userData[1].password
                self.db.updateUserProfile(user)
                return [True, "Profile Updated Succesfully"]
            else:
                return [False, "Incorrect password"]
        else:
            return [False, "User does not exist"]

    def changePassword(self, currentpassword, newpassword, confirmpassword, userid):
        if(newpassword != confirmpassword):
            return [False, "Confirm password did not match"]

        userData = self.db.getUserById(userid)

        if(userData[0]):
            if (bcrypt.checkpw(str(currentpassword).encode('utf-8'), str(userData[1].password).encode('utf-8'))):
                hashed = bcrypt.hashpw(
                    str(newpassword).encode('utf-8'), bcrypt.gensalt())
                self.db.updateUserPassword(hashed.decode(), userid)
                return [True, "Password updated succesfully"]
            else:
                return [False, "Incorrect Current password"]
        else:
            return [False, "User does not exist"]

    def validatePartner(self, selfUser):
        partner  = self.db.getUserById(selfUser.partner)
        if(partner[0] == False or partner[0] == selfUser):
            return [False, "Partner does not exist, Add Valid Partner to Get Started."]
        if(partner[1].partner != selfUser.userid):
            return [False, "Ask Your Partner to Add you Back to Get Started."]
        return [True, partner[1]]


    def getUserName(self, userid):
        userData = self.db.getUserById(userid)
        return userData[1].name

    def getNumberOfUsers(self):
        data = self.db.getNumberOfUsers()
        if(data[0]):
            return data[1]
        else:
            return 0
    
    def getAllUsers(self):
        data = self.db.getAllUsers()
        if(data[0]):
            return data[1]
        else:
            return 0

    def addMessage(self,message):
        data = self.db.getUserById(message["sender"])
        if(data[0]):
            if message["reciever"] in data[1].messages:
                data[1].messages[message["reciever"]].append(message)
            else:
                data[1].messages[message["reciever"]] = [message]
        self.db.updateUserMessages(data[1].messages,data[1].userid)

        data = self.db.getUserById(message["reciever"])
        if(data[0]):
            if message["sender"] in data[1].messages:
                data[1].messages[message["sender"]].append(message)
            else:
                data[1].messages[message["sender"]] = [message]

        self.db.updateUserMessages(data[1].messages,data[1].userid)