import instaloader
from flask import Flask, jsonify

app = Flask(__name__)

class GetInstagramProfile():
    def __init__(self) -> None:
        self.bot = instaloader.Instaloader()



    def get_basic_data(self, username):
        profile = instaloader.Profile.from_username(self.bot.context, username)

        responce = {"Username:": profile.username,
                    "User ID: ": profile.userid,
                    "Number of Posts:": profile.mediacount,
                    "Followers: ": profile.followers,
                    "Followees: ": profile.followees,
                    "Bio: ": profile.biography}
        return responce




cls = GetInstagramProfile()

@app.rout('/<username>')
def get_basic_info(username):
    return jsonify(cls.get_basic_data(username))
