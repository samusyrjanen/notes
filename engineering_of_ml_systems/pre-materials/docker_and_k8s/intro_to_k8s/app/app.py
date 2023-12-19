from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    user_info = {
        "user account": os.environ.get("USER_ACCOUNT", "default_user"),
        "password": os.environ.get("PASSWORD", "default_pwd")
    }
    return user_info

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)