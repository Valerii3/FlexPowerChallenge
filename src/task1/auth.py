from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

USER_DATA = {
    "Admin": "Password",
    "Username": "Password"
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password
