from flask import Blueprint, render_template, redirect, request, session
from flask.helpers import url_for
import random

user = Blueprint("user", __name__, static_folder="static",
                 template_folder="templates")


from User import UserModel, UserServices
from app import db


@user.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("index") is not None:
        return redirect(url_for('user.profile'))

    if (request.method == "POST"):

        form_data = request.form
        user = UserModel.User(None, None, None,form_data.get(
            "userid"), form_data.get("password"), None, None, None, None, None, None)

        userService = UserServices.UserServices(db)
        dataRequest = userService.login(user)

        if (dataRequest[0]):
            print("logged in successfully")
            session["index"] = dataRequest[1].index
            return redirect(url_for('home'))

        else:
            print("login failed")
            return render_template('login.html', warning=dataRequest[1])

    if (request.method == "GET"):
        return render_template('login.html')


@user.route('/editprofile', methods=['GET', 'POST'])
def editprofile():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name

    else:
        return redirect(url_for('user.login'))

    if (request.method == "POST"):

        form_data = request.form

        user = UserModel.User(userData[1].index, form_data.get("name"),form_data.get("gender"), userData[1].userid, form_data.get(
            "password"), userData[1].avatar, form_data.get("bio"), form_data.get("country"), form_data.get("DOB"), form_data.get("partner") ,userData[1].messages)
        userService = UserServices.UserServices(db)
        status = userService.editProfile(user)
        print(status[1])
        if(status[0]):
            return redirect(url_for('user.profile'))
        else:
            return render_template('editprofile.html', firstname=firstname, name=user.name, userid=user.userid, bio=user.bio, DOB=user.DOB, avatar=user.avatar, country=user.country, gender=userData[1].gender, partner=userData[1].partner ,warning=status[1])

    if (request.method == "GET"):
        if " " in name:
            firstname = name.split()[0]
            return render_template('editprofile.html', firstname=firstname, name=name, userid=userData[1].userid, bio=userData[1].bio, DOB=userData[1].DOB, avatar=userData[1].avatar, country=userData[1].country, gender=userData[1].gender, partner=userData[1].partner)


@user.route('/profile', methods=['GET'])
def profile():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
        userData = userService.getUserSession(session.get("index"))
        name = userData[1].name
        firstname = name

        if " " in name:
            firstname = name.split()[0]

        if (userData[0]):
            return render_template('profile.html', firstname=firstname, name=name, userid=userData[1].userid, bio=userData[1].bio, DOB=userData[1].DOB, avatar=userData[1].avatar, country=userData[1].country, gender=userData[1].gender, partner=userData[1].partner)
        else:
            return redirect(url_for('user.login'))

    return redirect(url_for('user.login'))


@user.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
        userData = userService.getUserSession(session.get("index"))
        if (userData[0]):
            name = userData[1].name
            firstname = name
            if " " in name:
                firstname = name.split()[0]

    else:
        return redirect(url_for('user.login'))

    if (request.method == "POST"):

        form_data = request.form
        currentpassword = form_data["currentpassword"]
        newpassword = form_data["newpassword"]
        confirmpassword = form_data["confirmpassword"]

        userService = UserServices.UserServices(db)
        status = userService.changePassword(
            currentpassword, newpassword, confirmpassword, userData[1].userid)
        print(status[1])
        if(status[0]):
            return render_template('changepassword.html', firstname=firstname, name=userData[1].name, bio=userData[1].bio, avatar=userData[1].avatar, gender=userData[1].gender,partner=userData[1].partner, message=status[1])
        else:
            return render_template('changepassword.html', firstname=firstname, name=userData[1].name, bio=userData[1].bio, avatar=userData[1].avatar, gender=userData[1].gender,partner=userData[1].partner, warning=status[1])

    if (request.method == "GET"):

        if (userData[0]):
            return render_template('changepassword.html', firstname=firstname, name=name, bio=userData[1].bio, avatar=userData[1].avatar, gender=userData[1].gender,partner=userData[1].partner)
        else:
            return redirect(url_for('user.login'))


@user.route('/messages', methods=['GET'])
def messages():
    if (not session.get("index") is None):
        userService = UserServices.UserServices(db)
        userData = userService.getUserSession(session.get("index"))
        name = userData[1].name
        firstname = name

        if " " in name:
            firstname = name.split()[0]

        if (userData[0]):
            partner = userService.validatePartner(userData[1])
            if(partner[0]):
                print(partner[1])
                return render_template('Messages.html', firstname=firstname,user=partner[1],selfUser=userData[1], warning="")
            else:
                return render_template('Messages.html', firstname=firstname,user=None,selfUser=userData[1], warning=partner[1])
        else:
            return redirect(url_for('user.login'))

    return redirect(url_for('user.login'))


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if (not session.get("index") is None):
        return redirect(url_for('user.profile'))
    if(request.method == "POST"):
        form_data = request.form
        userService = UserServices.UserServices(db)
        status = userService.validateData(form_data.get("name"), form_data.get("email"), form_data.get(
            "password"), form_data.get("confirmpassword"), form_data.get("DOB"), form_data.get("country"), form_data.get("gender"))
        if(not status[0]):
            return render_template("signup.html", warning=status[1])
        user = UserModel.User(None, form_data.get("name"), form_data.get("gender") ,form_data.get("email"), form_data.get(
            "password"), random.randint(1,5), "Add Bio", form_data.get("country"), form_data.get("DOB"),"Add Partner", {})
        status = userService.register(user)
        if(not status[0]):
            return render_template("signup.html", warning=status[1])
        return redirect(url_for('user.login'))
    if(request.method == "GET"):
        return render_template("signup.html")


@user.route('/signout', methods=['GET'])
def signout():
    userService = UserServices.UserServices(db)
    userService.signout()
    return redirect(url_for('home'))


@user.route('/', methods=['GET'])
def redir():
    return redirect(url_for('user.login'))
