from baseapp import app
from werkzeug.security import check_password_hash
from baseapp.models import Users
from baseapp.controllers import UsersController
from baseapp.forms import LoginForm, RegisterForm, UsersForm, UsersFormEdit
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask import render_template, request, redirect, url_for, abort


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route("/users/<int:page_num>")
@login_required
def users(page_num):
    if not current_user.admin:
        abort(401)

    users = Users.query.paginate(per_page=3, page=page_num, error_out=True)
    return render_template('users.html', username=current_user.username, users=users)

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
@login_required
def user(user_id):
    if not current_user.admin:
        abort(401)

    msg = ""
    form = UsersFormEdit()
    user = Users.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        userc = UsersController()
        user_data = {}
        if form.delete.data == 'Y':
            user_data['id'] = user.id
            userc.delete(user_data)
            return redirect(url_for('users',page_num=1))
        else:
            user_data['username'] = form.username.data
            user_data['email'] = form.email.data
            user_data['id'] = user.id
            userc.edit(user_data)
            return redirect(url_for('users',page_num=1))


    form.username.data = user.username
    form.email.data = user.email
    delete = request.args.get('delete', None)
    if delete:
        form.delete.data = 'Y'
    else:
        form.delete.data = 'N'

    return render_template('user.html', username=current_user.username, form=form, uid=user.id)

@app.route("/user/add", methods=["GET", "POST"])
@login_required
def adduser():
    if not current_user.admin:
        abort(401)

    form = UsersForm()
    if form.validate_on_submit():
        userc = UsersController()
        user_data = {}
        user_data['username'] = form.username.data
        user_data['email'] = form.email.data
        user_data['password'] = form.password.data
        userc.add(user_data)
        return redirect(url_for('users', page_num=1))

    return render_template('register.html', form=form)


@app.route("/login",methods=["GET","POST"])
def login():
    msg = ""
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
        msg = "Invalid username or password!"

    return render_template('login.html', form=form, msg=msg)

@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    form = LoginForm()
    return redirect(url_for('login'))


