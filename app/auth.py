from flask import Blueprint,render_template,redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user 
from werkzeug.security import check_password_hash
from .extensions import login,db
from .forms import LoginForm
from .models import User

auth_bp=Blueprint("auth",__name__)
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@auth_bp.route("/login",methods=["GET","POST"])
def login():
      form=LoginForm()
      if form.validate_on_submit():
          user=User.query.filter_by(username=form.username.data).first()
          if user and check_password_hash(
              user.password_hash,
              form.password.data
          ):
              login_user(user)
              return redirect(url_for("main.enquiry"))
          flash("Invalid username or password.")
      return render_template("login.html", form=form)
@auth_bp.route("/logout")
@login_required
def logout():
     logout_user()
     return redirect(url_for("auth.login"))
     