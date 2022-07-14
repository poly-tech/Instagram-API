import instaloader
from flask import Flask, jsonify, send_file, request
import os

app = Flask(__name__)

class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()
        self.followers = []
        self.following = []
        self.comments = []

    def download_users_profile_picture(self, username):
        self.L.download_profile(username, profile_pic_only=True)
        return f"./{username}/{os.listdir(f'./{username}')[0]}"



    def get_basic_data(self, username):
        profile = instaloader.Profile.from_username(self.L.context, username)

        response = {"Username:": profile.username,
                    "User ID: ": profile.userid,
                    "Number of Posts:": profile.mediacount,
                    "Followers: ": profile.followers,
                    "Followees: ": profile.followees,
                    "Bio: ": profile.biography}
        return response

    def get_users_followers(self,username, id, password):
        '''
        returns the lists of the target's (username) followers
        Note: login required to get a profile's followers.
        args:
            username : The account title you want to scrape data from.
            id: your own username.
            password: your own password.
        '''
        self.L.login(id, password)

        profile = instaloader.Profile.from_username(self.L.context, username)
        for follower in profile.get_followers():
            username = follower.username
            self.followers.append(username)
        return self.following

    def get_users_followings(self, username, your_username, your_password):
        '''
        returns the lists of the target's (username) followings
        Note: login required to get a profile's followers.
        args:
            username : The account title you want to scrape data from.
            id: your own
            password: your own password
        '''
        self.L.login(your_username, your_password)
        profile = instaloader.Profile.from_username(self.L.context, username)
        for following in profile.get_followees():
            username = following.username
            self.followers.append(username)
        return self.followers


cls = GetInstagramProfile()

# @app.route('/username=<username>&password=<password>&id=<id>')
# # @app.route('/<username>,id=<id>,password=<password>')
# def get_basic_info(username, password, id):

@app.route('/search', methods=['GET'])
def search():
    args = request.args
    # All comments under this function are still in testing
    username = args.get('username')
    id = args.get('id')
    password = args.get('password')

    # response = {'username':username,
    #             'id':id,
    #             'password':password}

    response = cls.get_basic_data(username)

    if not (id == '' or password == ''):
        response['followers'] = cls.get_users_followers(username, id, password)
        response['following'] = cls.get_users_followings(username, id, password)

    #localhost:5000/search?username=username&id=id&password=password
    return jsonify(response), 200
    # return jsonify(response)

@app.route('/download_profile_img/<username>')
def download_profile_img(username):

    return send_file(cls.download_users_profile_picture(username))








app.run(debug=True)
