import base64
import hashlib
import requests
import secrets

from flask import Flask, render_template, redirect, request, session, url_for
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask(__name__)
app.config.update({'SECRET_KEY': secrets.token_hex(64)})
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
from user import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("signin.html")

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

config = {
    "auth_uri": "https://dev-53586631.okta.com/oauth2/default/v1/authorize",
    "client_id": "0oad1vc2twMXqUTqh5d7",
    "client_secret": "3zci627rAC-4JQfonXKjdOosv4m3wlceQ0P3wmV0NNI69zjJrMLAhEtgb4wtc6kJ",
    "redirect_uri": "http://localhost:5000/authorization-code/callback",
    "issuer": "https://dev-53586631.okta.com/oauth2/default",
    "token_uri": "https://dev-53586631.okta.com/oauth2/default/v1/token",
    "userinfo_uri": "https://dev-53586631.okta.com/oauth2/default/v1/userinfo"
}


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')  # Get the email from the form
        password = request.form.get('password')  #
        if email and password:
            # Successful sign-in, redirect to the "profile" page
            return redirect(url_for('profile'))
        else:
            return 'Invalid email or password'  # Handle invalid credentials

    # If it's a GET request, this block will run and render the sign-in form
    return render_template('signin.html')


@app.route("/signout", methods=["GET", "POST"])
@login_required
def signout():
    logout_user()
    return redirect(url_for("signin"))

@app.route("/authorization-code/callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    code = request.args.get("code")
    app_state = request.args.get("state")
    if app_state != session['app_state']:
        return "The app state doesn't match"
    if not code:
            return "The code wasn't returned or isn't accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url,
                    'code_verifier': session['code_verifier'],
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
            return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    # Authorization flow successful, get userinfo and sign in user
    userinfo_response = requests.get(config["userinfo_uri"],
                                    headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
            User.create(unique_id, user_name, user_email)

    login_user(user)

    return redirect(url_for("profile"))

@app.route("/profile")
def profile():
    return render_template("profile.html", user=current_user)


  