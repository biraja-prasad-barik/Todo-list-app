from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

USER_CREDENTIALS = {
    'username': 'Biraja',
    'password': '1234'
}

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
            session['user'] = username
            flash('Login Successful!', 'success')
            # Login ke baad user ko tasks page ya home page par bhej dein
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid username and password', 'danger')
            # Agar login fail hua to wapas login page dikhayein
            return redirect(url_for('auth.login'))
            
    # Agar method GET hai to login page dikhayein
    return render_template("login.html")

# Yeh function ab login function ke bahar hai, isliye yeh sahi se kaam karega
@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info') # Spelling theek ki hai
    return redirect(url_for('auth.login'))