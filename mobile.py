"""
    File Name       :   mobile.py
    Project         :   Bot
    Created On      :   APR 18 2020
    Last Modified   :   APR 300 2020
    Author          :   Yash Gohel <yashgohel16@gmail.com>
    Developer       :   Planck
"""
import json
import time
import random
import string
import uuid
import urllib.request
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from igramscraper import instagram

class Bot(object):
    def __init__(self, username, password):
        self.browser_profile = webdriver.ChromeOptions()
        self.browser_profile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        mobile_emulation = { "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 }, "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
        self.browser_profile.add_experimental_option('mobileEmulation', mobile_emulation)
        # self.browser_profile.add_argument('headless')
        self.browser = webdriver.Chrome('includes/chromedriver.exe', chrome_options=self.browser_profile)
        self.username = username
        self.password = password
        self.ig = instagram.Instagram()

        # Default wait time
        self.rest = 3
        # Default limit value
        self.limit = 10
        self.list_limit = 300
        self.list_follower_limit = 6
        self.list_following_limit = 50
        self.like_limit = 20
        self.comment_limit = 5
        self.follow_limit = 20
        self.unfollow_limit = 20
        self.confirm_limit = 80
        self.download_limit = 100
        self.rest_time = 60
        self.delete_limit = 10

    def generateRandomId(self):
        length = 64
        pool = string.ascii_lowercase
        return ''.join(random.choice(pool) for i in range(length))

    def addRecord(self, uid, _type, value):
        url = 'http://localhost/planck/bot/record.php?request=add_record'
        self.browser.get(url + '&uid=' + uid + '&type=' + _type + '&value=' + value)
        time.sleep(1)
        print('Record added')

    def startTask(self, username, task, tid, _max, _value=None):
        url = 'http://localhost/planck/bot/record.php?request=start_task'
        urllib.request.urlopen(url + '&uid=' + username + '&task=' + task + '&tid=' + tid + '&max=' + str(_max) + '&tvalue=' + _value)

    def updateTask(self, tid):
        url = 'http://localhost/planck/bot/record.php?request=update_task'
        urllib.request.urlopen(url + '&tid=%27' + tid + '%27')

    def endTask(self, tid):
        url = 'http://localhost/planck/bot/record.php?request=end_task'
        urllib.request.urlopen(url + '&tid=%27' + tid + '%27')

    def addInstagramUser(self, uname, user, stat, extra):
        url = 'http://localhost/planck/bot/request.php?request=add_instagram_user'
        urllib.request.urlopen(url + '&aname=' + self.username + '&uname=' + uname + '&user=' + user + '&stat=' + stat + '&extra=' + extra)

    def updateIGCache(self, csrftoken, ds_user_id, sessionid, mid):
        url = 'http://localhost/planck/bot/record.php?request=update_igcache&'
        par = url + 'uid=' + self.username + '&csrftoken=' + csrftoken + '&ds_user_id=' + ds_user_id + '&sessionid=' + sessionid + '&mid=' + mid
        urllib.request.urlopen(par)


    # Instagram login
    def login(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        # Get input element
        username_input = self.browser.find_elements_by_css_selector('form input')[0]
        password_input = self.browser.find_elements_by_css_selector('form input')[1]
        # Set input element
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        # Hit login button
        password_input.send_keys(Keys.ENTER)
        print('Login successfully')

    def reLogin(self):
        self.browser.get('https://www.instagram.com')
        username = self.username
        for i in ['.', '@', '_']:
            username = username.replace(i, '-')
        path = 'cache/session/'+ self.username + '/' + username + '.txt'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                login = json.load(f)
                csrftoken = login['csrftoken']
                ds_user_id = login['ds_user_id']
                sessionid = login['sessionid']
                mid = login['mid']
                self.updateIGCache(csrftoken, ds_user_id, sessionid, mid)
                self.browser.delete_cookie("csrftoken")
                self.browser.delete_cookie("ds_user_id")
                self.browser.delete_cookie("sessionid")
                self.browser.delete_cookie("mid")
                self.browser.add_cookie({"name": "csrftoken", "value": csrftoken, 'sameSite': 'Strict'})
                self.browser.add_cookie({"name": "ds_user_id", "value": ds_user_id, 'sameSite': 'Strict'})
                self.browser.add_cookie({"name": "sessionid", "value": sessionid, 'sameSite': 'Strict'})
                self.browser.add_cookie({"name": "mid", "value": mid, 'sameSite': 'Strict'})
                f.close()
                time.sleep(3)
        except IOError:
            print('File not found')
            self.login()
        

    # Close notification dialog
    def close_notification_dialog(self):
        try:
            self.browser.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
        except NoSuchElementException:
            print('Element not found')

     # Close notification dialog
    def close_notification_dialog2(self):
        try:
            self.browser.find_element_by_xpath("//button[contains(text(),'Cancel')]").click()
        except NoSuchElementException:
            print('Element not found')

    def deletePosts(self):
        try:
            task = 'delete-posts'
            tid = self.generateRandomId()
            self.browser.find_elements_by_css_selector('.gKAyB')[3].click()
            print("profile")
            time.sleep(3)
            _max = self.delete_limit
            self.startTask(self.username, task, tid, _max, self.username)
            i = 0
            while i < _max:
                post = self.browser.find_elements_by_css_selector('._9AhH0')
                print("list")
                post[0].click()
                print("click")
                time.sleep(2)
                self.browser.find_element_by_css_selector('.MEAGs .wpO6b').click()
                print("menu")
                time.sleep(1)
                self.browser.find_elements_by_css_selector('.aOOlW')[0].click()
                time.sleep(1)
                self.browser.find_elements_by_css_selector('.aOOlW')[0].click()
                self.updateTask(tid)
                print(f'{i} post deleted')
                i += 1
                time.sleep(2)
            self.endTask(tid)
        except NoSuchElementException:
            print('Element not found')

    def viewStory(self, hastag):
        try:
            task = 'view-hastag-story'
            tid = self.generateRandomId()
            self.browser.get('https://www.instagram.com/explore/tags/' + hastag)
            time.sleep(self.rest)
            max_limit = self.limit
            print(max_limit)
            self.browser.find_elements_by_css_selector('.aoVrC')[0].click()
            time.sleep(self.rest)
            st = self.browser.find_elements_by_css_selector('._7zQEa')
            if max_limit > len(st):
                max_limit = len(st)
            self.startTask(self.username, task, tid, max_limit, hastag)
            i = 0
            while i < max_limit:
                time.sleep(1)
                self.browser.find_element_by_css_selector('.NnZaL').click()
                i = i + 1
                print(f'{i} story viewed')
                self.updateTask(tid)
            self.endTask(tid)
        except NoSuchElementException:
            print('Element not found')

    def get_common_followers(self, username):
        common = []
        for i in self.read_followers(username):
            if i in self.read_following(username):
                common.append(i)
        return common

    def get_none_followers(self, username):
        followers = self.read_followers(username)
        following = self.read_following(username)
        common = self.get_common_followers(username)

        for i in following:
            if i in followers:
                following.remove(i)

        for i in following:
            if i in common:
                following.remove(i)

        return following

    # Fanbase
    def get_none_following(self, username):
        followers = self.read_followers(username)
        following = self.read_following(username)
        common = self.get_common_followers(username)

        for i in followers:
            if i in following:
                followers.remove(i)

        for i in followers:
            if i in common:
                followers.remove(i)

        return followers

    def insert_db_user_info(self, username):
        follower = self.read_followers(username)
        following = self.read_following(username)
        for i in follower:
            self.getUserInfo(i)
        for i in following:
            self.getUserInfo(i)
        print("Insert success for users info")

    def save_unfollowed(self, _list):
        path = 'output/' + self.username + '-unfollowed.json'
        user = {'username': self.username, 'unfollowed': _list}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    # Save JSON file with user details like followers and following data
    def save_file(self, followers, followings, username):
        path = 'output/' + username + '.json'
        user = {'username': username, 'followers': followers, 'following': followings}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)
        time.sleep(3)
        self.save_common_followers(username)
        time.sleep(3)
        self.save_none_followers(username)
        time.sleep(3)
        self.insert_db_user_info(username)


    def save_none_followers(self, username):
        c = self.get_none_followers(username)
        path = 'output/' + username + '-none.json'
        user = {'none': c}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    def save_none_following(self, username):
        c = self.get_none_following(username)
        path = 'output/' + username + '-fan.json'
        user = {'fan': c}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    def save_common_followers(self, username):
        c = self.get_common_followers(username)
        path = 'output/' + username + '-common.json'
        user = {'common': c}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    # Get followers data from the JSON file
    def read_followers(self, username):
        path = 'output/' + username + '.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                user_file = json.load(f)
                user_followers = user_file['followers']
                f.close()
                # print(user_followers)
        except IOError:
            print('File not found on local disk fetching from server')
            user_followers = self.getUserFollowers(username)
        return user_followers

    # Get following data from JSON file
    def read_following(self, username):
        path = 'output/' + username + '.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                user_file = json.load(f)
                user_following = user_file['following']
                f.close()
                # print(user_following)
        except IOError:
            print('File not found on local disk fetching from server')
            user_following = self.getUserFollowing(username)
        return user_following

    # Get user list who not follow back you
    def read_none_followers(self, username):
        path = 'output/' + username + '-none.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                user_file = json.load(f)
                user_none = user_file['none']
                f.close()
                print(user_none)
        except IOError:
            print('File not found on local disk fetching from server')
            user_none = self.get_none_followers(username)      
        return user_none

    def read_none_following(self, username):
        path = 'output/' + username + '-fan.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                user_file = json.load(f)
                user_fan = user_file['fan']
                f.close()
                print(user_fan)
        except IOError:
            print('File not found on local disk fetching from server')
            user_fan = self.get_none_following(username)
        return user_fan

    def read_common_followers(self, username):
        path = 'output/' + username + '-common.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                user_file = json.load(f)
                user_common = user_file['common']
                f.close()
                print(user_common)
        except IOError:
            print('File not found on local disk fetching from server')
            user_common = self.get_common_followers(username)
        return user_common

    # Close browser it self
    def close_browser(self):
        print('Session end')
        self.browser.quit()

    # Terminate process
    def __exit__(self, exc_type, exc_value, traceback):
        self.close_browser()


    def userLogin(self):
        path = "cache/session/" + self.username + "/"
        self.ig.with_credentials(self.username, self.password, path)
        self.ig.login(force=False,two_step_verificator=True)
        time.sleep(2) 

    # Useing pre coded function by other developers
    def getUserInfo(self, user):
        self.userLogin()
        account = self.ig.get_account(user)
        return account
        # self.get_user_info(account)

    def getUserFollowers(self, user, login=True):
        self.userLogin()
        followers = []
        _list = []
        account = self.ig.get_account(user)
        time.sleep(1)
        followers = self.ig.get_followers(account.identifier, self.list_follower_limit, self.list_follower_limit, delayed=False) 
        for follower in followers['accounts']:
            _list.append(follower.username)
        return _list

    def getUserFollowing(self, user, login=True):
        self.userLogin()
        followings = []
        _list = []
        account = self.ig.get_account(user)
        time.sleep(1)
        followings = self.ig.get_following(account.identifier, self.list_following_limit, self.list_following_limit, delayed=False) 
        for following in followings['accounts']:
            _list.append(following.username)
        return _list

    def downloadPost(self, user):
        # self.userLogin()
        post = []
        medias = self.ig.get_medias("itsevilword", self.download_limit)
        for m in medias:
            post.append(m.image_high_resolution_url)
        return post

    # Save JSON file with user details like followers and following data
    def saveFile(self, user):
        f1 = self.getUserFollowers(user)
        print(f1)
        f2 = self.getUserFollowing(user)
        print(f2)
        follower = []
        follwing = []
        for i in f1:
            follower.append(str(i))
        for i in f2:
            follwing.append(str(i))

        path = 'output/' + user + '.json'
        user = {'username': user, 'followers': follower, 'following': follwing }
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)
        time.sleep(3)
        self.save_common_followers(user)
        time.sleep(3)
        self.save_none_followers(user)
        time.sleep(3)

    
    def updateUserData(self):
        account = self.getUserInfo(self.username)
        print(account)
        path = 'output/info/' + self.username + '.json'
        user = { 
            'username': self.username, 
            'followers': account.followed_by_count, 
            'following': account.follows_count, 
            'post': account.media_count,
            'name': account.full_name,
            'dp': account.get_profile_picture_url()
        }
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)
