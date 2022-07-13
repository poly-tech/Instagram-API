import instaloader
from flask import Flask, jsonify

app = Flask(__name__)

class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()
        self.followers = []
        self.following = []



    def get_basic_data(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)

        responce = {"Username:": profile.username,
                    "User ID: ": profile.userid,
                    "Number of Posts:": profile.mediacount,
                    "Followers: ": profile.followers,
                    "Followees: ": profile.followees,
                    "Bio: ": profile.biography}
        return responce

    def get_users_followers(self,user_name, id, password):
        '''Note: login required to get a profile's followers.'''
        self.L.login(id, password)

        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("follower_names.txt","a+")
        for follower in profile.get_followers():
            username = follower.username
            file.write(username + "\n")
            self.followers.append(username)
        return self.following

    def get_users_followings(self, user_name, your_username, your_password):
        '''Note: login required to get a profile's followings. Enter Your USERNAME AND PASSWORD'''
        self.L.login(your_username, your_password)
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open("following_names.txt","a+")
        for following in profile.get_followees():
            username = following.username
            file.write(username + "\n")
            self.followers.append(username)
        return self.followers




cls = GetInstagramProfile()

@app.route('/username=<username>,password=<password>,id=<id>')

def get_basic_info(username, id, password):
    # return jsonify({'username':username, 'id':id, 'password':password})


    responce = cls.get_basic_data(username)

    if not (id == '' or username == ''):
        responce['followers'] = cls.get_users_followers(username, id, password)
        responce['following'] = cls.get_users_followings(username, id, password)

    return jsonify(responce), 200





app.run(debug=True)
