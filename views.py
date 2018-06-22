from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user

from ballista import app, db, login_manager
from ballista.models import User, Rifle, Round, Caliber
from ballista.forms import LoginForm, AddRifleForm


# TODO: Add A Round
# TODO: Add a caliber (on round page, if Caliber not in list)
# TODO: Delete Rifle, Round


# ================
# Login Management
# ================
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


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


@app.route('/')
@app.route('/index')
@login_required
def index():
    cur_rifle = Rifle.query.filter_by(id=current_user.selected_rifle).first()
    cur_round = Round.query.filter_by(id=current_user.selected_round).first()
    return render_template('index.html', cur_rifle=cur_rifle, cur_round=cur_round)


# =========================
# Primary Pages & Resources
# =========================
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
def set_rifle(rifle_id):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    rifle = Rifle.query.filter_by(id=rifle_id, user_id=user.id).first_or_404()
    user.selected_rifle = rifle.id
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):  # Rifle List to set rifle
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/set_round/<round_id>')
@login_required
def set_round(round_id):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    if user.selected_rifle is None:
        flash(f"Select a Rifle Prior to Selecting a Round")
        return redirect(url_for('index'))
    else:
        rnd = Round.query.filter_by(id=round_id).first_or_404()
        user.selected_round = rnd.id
        db.session.commit()
        flash(f"Round Set")
        return redirect(url_for('index'))


@app.route('/<rifle_id>/rounds')
@login_required
def rifle_rounds(rifle_id):
    if current_user.selected_rifle is None:
        flash(f"Select a Rifle Prior to Selecting a Round")
        return redirect(url_for('index'))
    else:
        rifle = Rifle.query.filter_by(id=rifle_id, user_id=current_user.id).first_or_404()
        caliber = Caliber.query.filter_by(id=rifle.caliber_id).first_or_404()
        return render_template('rifle_rounds_base_page.html', rifle=rifle, caliber=caliber)


# ================================
# Other Resources
# ================================


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
