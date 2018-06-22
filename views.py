from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_required, login_user, logout_user, current_user

from ballista import app, db, login_manager
from ballista.models import User, Rifle
from ballista.forms import LoginForm, AddRifleForm#, SelectRifleForm

# TODO: Select Rifle Form
# TODO: IF SelectedRifle = None THEN select a rifle
# TODO: Select Round Form
# TODO: IF SelectedRound = None THEN select a round


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('index',
                            username=user.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop('selected_rifle', None)
    session.pop('selected_round', None)

    logout_user()
    return redirect(url_for('index'))


@app.route('/rifle/add', methods=['GET', 'POST'])
@login_required
def add_rifle():
    form = AddRifleForm()
    if form.validate_on_submit():
        name = form.name.data
        caliber = form.caliber.data
        barrel_length = form.barrel_length.data
        rfl = Rifle(name=name, caliber_id=caliber, barrel_length=barrel_length, user_id=current_user.id)

        db.session.add(rfl)
        db.session.commit()
        flash(f"Stored '{rfl.name}")
        return redirect(url_for('index'))
    return render_template('add_rifle.html', form=form, title='Add a Rifle')


@app.route('/rifle/set/<rifle_id>')
@login_required
def set_rifle():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return redirect(url_for('index'))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
