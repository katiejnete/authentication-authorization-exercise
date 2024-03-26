"""Authentication Authorization Exercise - Flask Feedback."""

from flask import Flask, render_template, redirect, request, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
from secret import SECRET_KEY
import sqlalchemy.exc


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = SECRET_KEY

connect_db(app)
app.app_context().push()


@app.route("/")
def redirect_register():
    """Redirects user to /register."""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_form_handler():
    """Shows and handles register form."""

    form = RegisterUserForm()

    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            new_user = User.register_user(
                username, password, email, first_name, last_name
            )
            db.session.add(new_user)
            try:
                db.session.commit()
                session["username"] = username
                return redirect(f"/users/{username}")
            except sqlalchemy.exc.IntegrityError as err:
                if "(username)" in err.args[0]:
                    flash("Username taken.")
                elif "(email)" in err.args[0]:
                    flash("E-mail taken.")
                return render_template("register_form.html", form=form)
    else:
        return render_template("register_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_form_handler():
    """Shows and handles login form."""

    form = LoginUserForm()

    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.authenticate_user(username, password)

            if isinstance(user, User):
                session["username"] = user.username
                return redirect(f"/users/{user.username}")
            else:
                flash(user)
    return render_template("login_form.html", form=form)


@app.route("/users/<username>")
def show_user(username):
    """Shows information about user."""

    try:
        if session["username"] == username:
            user = db.get_or_404(User, username)
            feedback = Feedback.get_user_feedback(username)
            return render_template("user_page.html", user=user, feedback=feedback)
        else:
            flash('Unauthorized action.')
            return redirect(f"/users/{session["username"]}")
    except KeyError:
        flash("Please login to view page.")
        return redirect("/login")


@app.route("/logout")
def logout_user():
    """Logout user. Redirect to homepage."""

    try:
        session.pop("username")
        flash("Logged out.")
        return redirect("/")
    except KeyError:
        return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def feedback_form_handler(username):
    """Shows and handles feedback form."""

    form = FeedbackForm()

    try:
        if session["username"] == username:
            user = db.get_or_404(User, username)
            if request.method == "POST":
                if form.validate_on_submit():
                    title = form.title.data
                    content = form.content.data
                    new_feedback = Feedback(title=title, content=content, username=username)
                    db.session.add(new_feedback)
                    db.session.commit()
                    return redirect(f"/users/{username}")
            return render_template("feedback_form.html", form=form, user=user)
        else:
            flash('Unauthorized action.')
            return redirect(f"/users/{session["username"]}")            
    except KeyError:
        flash("Please login to view page.")
        return redirect("/login")
    
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Removes user from db."""

    try:
        if session["username"] == username:
            user = db.get_or_404(User,username)
            db.session.delete(user)
            db.session.commit()
            session.pop("username")
            flash("User deleted.")
            return redirect("/")
        else:
            flash("Unauthorized action.")
            return redirect(f"/users/{session["username"]}")
    except KeyError:
        flash("Please login to complete action.")
        return redirect("/login")

@app.route("/feedback/<int:feedback_id>/update", methods=["GET","POST"])
def update_feedback(feedback_id):
    """Update feedback."""

    fb = db.get_or_404(Feedback, feedback_id)
    form = FeedbackForm(obj=fb)
    user = User.find_user(feedback_id)

    try:
        if session["username"] == user.username:
            if request.method == "POST":
                if form.validate_on_submit():
                    fb.title = form.title.data
                    fb.content = form.content.data
                    db.session.commit()
                    return redirect(f"/users/{user.username}")
            return render_template("update_feedback.html", form=form, user=user, feedback=fb)
        else:
            flash("Unauthorized action.")
            return redirect(f"/users/{session["username"]}")
    except KeyError:
        flash("Please login to complete action.")
        return redirect("/login")
    
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Deletes feedback from db."""

    fb = db.get_or_404(Feedback, feedback_id)
    user = User.find_user(feedback_id)

    try:
        if session["username"] == user.username:
            db.session.delete(fb)
            db.session.commit()
            flash("Feedback deleted.")
            return redirect(f"/users/{user.username}")
        else:
            flash("Unauthorized action.")
            return redirect(f"/users/{session["username"]}")
    except KeyError:
        flash("Please login to complete action.")
        return redirect("/login")

@app.route("/feedback/<int:feedback_id>")
def show_feedback(feedback_id):
    """Show feedback page."""

    feedback = db.get_or_404(Feedback, feedback_id)
    return render_template("feedback_page.html", feedback=feedback)