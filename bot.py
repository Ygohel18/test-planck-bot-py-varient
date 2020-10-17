"""
    File Name       :   bot.py
    Project         :   Bot
    Created On      :   APR 18 2020
    Last Modified   :   MAY 06 2020
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
    def __init__(self, username, password, open=False):
        if open == True:
            self.browser_profile = webdriver.ChromeOptions()
            self.browser_profile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            # self.browser_profile.add_argument('headless')
            #proxy = "205.185.115.100:8080"
            #self.browser_profile.add_argument('--proxy-server=%s' % proxy)
            self.browser = webdriver.Chrome('', chrome_options=self.browser_profile)
        self.username = username
        self.password = password
        self.ig = instagram.Instagram()

        # Default wait time
        self.rest = 3
        # Default limit value
        self.limit = 20
        self.list_limit = 120
        self.list_follower_limit = 1000
        self.list_following_limit = 1000
        self.like_limit = 20
        self.comment_limit = 5
        self.follow_limit = 20
        self.unfollow_limit = 100
        self.confirm_limit = 50
        self.download_limit = 10000
        self.rest_time = 900
        self.normal_rest_time = 3
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

    def startTask(self, username, task, tid, _max, _value="None"):
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

    def loginAdmin(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        # Get input element
        username_input = self.browser.find_elements_by_css_selector('form input')[0]
        password_input = self.browser.find_elements_by_css_selector('form input')[1]
        # Set input element
        username_input.send_keys("pravindabhi1934")
        password_input.send_keys("1811@vish")
        # Hit login button
        password_input.send_keys(Keys.ENTER)
        print('Login successfully')

    def updateIGCache(self, csrftoken, ds_user_id, sessionid, mid):
        url = 'http://localhost/planck/bot/record.php?request=update_igcache&'
        par = url + 'uid=' + self.username + '&csrftoken=' + csrftoken + '&ds_user_id=' + ds_user_id + '&sessionid=' + sessionid + '&mid=' + mid
        urllib.request.urlopen(par)


    def saveRemoteSession(self):
        username = self.username
        url = 'http://localhost/planck/bot/record.php?request=get_ig_session&token=809OHKZ73JOVVRFV&'
        par = url + 'username=' + username
        with urllib.request.urlopen(par) as response:
            source = response.read()
            data = json.loads(source)
            csrftoken = data['csrftoken']
            ds_user_id = data['ds_user_id']
            sessionid = data['sessionid']
            mid = data['mid']
            duser = data['appuser']
            uid = data['uid']
            username = data['username']

            session = {
                'appuser': duser,
                'uid': uid,
                'username': username,
                'csrftoken': csrftoken,
                'ds_user_id': ds_user_id,
                'sessionid': sessionid,
                'mid': mid
            }

            path = 'cache/session/'
            upath = path + '/' + username + '/'

            if not os.path.exists(upath):
                os.makedirs(upath)

            user = username.replace('_', '-')
            user = user.replace('.', '-')
            save = upath + user + '.txt'

            with open(save, 'w', encoding='utf-8') as fi:
                json.dump(session, fi, ensure_ascii=False)
            

    def dbLogin(self):
        username = self.username
        url = 'http://localhost/planck/bot/record.php?request=get_ig_session&token=809OHKZ73JOVVRFV&'
        par = url + 'username=' + username
        with urllib.request.urlopen(par) as response:
            source = response.read()
            data = json.loads(source)
            print(data)
            csrftoken = data['csrftoken']
            ds_user_id = data['ds_user_id']
            sessionid = data['sessionid']
            mid = data['mid']
            self.browser.get('https://www.instagram.com/'+username)
            self.browser.delete_cookie("csrftoken")
            self.browser.delete_cookie("ds_user_id")
            self.browser.delete_cookie("sessionid")
            self.browser.delete_cookie("mid")
            self.browser.delete_all_cookies()
            self.browser.add_cookie({"name": "csrftoken", "value": csrftoken, 'sameSite': 'Strict'})
            self.browser.add_cookie({"name": "ds_user_id", "value": ds_user_id, 'sameSite': 'Strict'})
            self.browser.add_cookie({"name": "sessionid", "value": sessionid, 'sameSite': 'Strict'})
            self.browser.add_cookie({"name": "mid", "value": mid, 'sameSite': 'Strict'})
            #self.browser.get('https://www.instagram.com/'+username)

    def getUsernameFromIg(self):
        self.browser.get('https://www.instagram.com')
        username = self.username
        url = 'http://localhost/planck/bot/record.php?request=get_username&token=809OHKZ73JOVVRFV&'
        par = url + 'username=' + username
        with urllib.request.urlopen(par) as response:
            source = response.read()
            data = json.loads(source)
            return data['username']

    def reLogin(self):
        self.saveRemoteSession()
        self.browser.get('https://www.instagram.com/accounts/login/')
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
                print(login)
                #self.browser.delete_cookie("csrftoken")
                #self.browser.delete_cookie("ds_user_id")
                #self.browser.delete_cookie("sessionid")
                #self.browser.delete_cookie("mid")
                self.browser.add_cookie({"name": "csrftoken", "value": csrftoken, 'sameSite': 'Strict'})
                self.browser.add_cookie({"name": "ds_user_id", "value": ds_user_id, 'sameSite': 'Strict'})
                self.browser.add_cookie({"name": "sessionid", "value": sessionid, 'sameSite': 'Strict'})
                self.browser.add_cookie({"name": "mid", "value": mid, 'sameSite': 'Strict'})
                f.close()
        except IOError:
            print('Session not found')
            #self.dbLogin()

    
    # Close notification dialog
    def close_notification_dialog(self):
        time.sleep(self.rest)
        try:
            self.browser.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
        except NoSuchElementException:
            print('Element not found')

    def saveDp(self, username, src):
        path = '../../../../cdn/bot/public/download/profile/'
        if not os.path.exists(path):
            os.makedirs(path)
        urllib.request.urlretrieve(src, path + username + ".jpg")

    def blockUser(self, username):
        try:
            self.browser.get('https://www.instagram.com/' + username + '/')
            time.sleep(self.rest)
            self.browser.find_element_by_css_selector('.AFWDX > button').click()
            self.browser.find_element_by_xpath("//button[contains(text(),'Block this user')]").click()
            self.browser.find_element_by_xpath("//button[contains(text(),'Block')]").click()
        except NoSuchElementException:
            print('Element not found')

    def checkGhostFollower(self, username):
        path = "cache/master/session/"
        self.ig.with_credentials("pravindabhi1934", "1811@vish", path)
        self.ig.login(force=False,two_step_verificator=True)
        account = self.ig.get_account(username)
        followers = account.followed_by_count
        following = account.follows_count
        #post = account.media_count
        count = followers/following

        if (count > 1):
            flag = True
        
        return flag


    def blockGhostFollowers(self):
        followers = self.get_user_followers(self.username)
        for f in followers:
            if(self.checkGhostFollower(f)):
                self.blockUser(f)

    # Get user basic details
    def get_user_info(self, account):
        try:
            profile = account.get_profile_picture_url()
            urllib.request.urlretrieve(profile, "assets/img/profile/" + account.username + ".jpg")
            image_url = "assets/img/profile/" + account.username + ".jpg"

            data = [
                account.username,
                image_url,
                account.media_count,
                account.followed_by_count,
                account.follows_count
            ]

            url = 'http://localhost/bot/record.php?request=add_user_info'
            self.browser.get(url + '&username=' + data[0] + '&profile=' + data[1] + '&post=' + data[2] + '&followers=' + data[3] + '&following=' + data[4])
            time.sleep(1)
        except NoSuchElementException:
            print('Element not found')


    # Follow user with username
    def follow_user(self, user):
        try:
            self.browser.get('https://www.instagram.com/' + user + '/')
            time.sleep(self.rest)
            button = self.browser.find_elements_by_css_selector('button')
            follow = button[0]
            if follow.text != 'Following':
                if follow.text != 'Requested':
                    follow.click()
                    print('User followed or requested')
                else:
                    print('You already requested this user')
            else:
                print('You are already following this user')
        except NoSuchElementException:
            print('Element not found')

    # Unfollow user with username
    def unfollow_user(self, user):
        try:
            self.browser.get('https://www.instagram.com/' + user + '/')
            time.sleep(self.rest)
            button = self.browser.find_elements_by_css_selector('button')
            unfollow = button[1]
            unfollow.click()
            self.browser.find_element_by_css_selector('.-Cab_').click()
            print('User unfollowed')
        except NoSuchElementException:
            print('Element not found')

    # Follow mass users
    def mass_follow(self, list):
        h = 0
        l = 0
        task = 'mass-follow'
        tid = self.generateRandomId()
        #self.startTask(self.username, task, tid, len(list))
        for i in list:
            if l < self.follow_limit:
                if h < self.limit:
                    self.follow_user(i)
                    #self.updateTask(tid)
                    print(f'{i} user followed')
                    h += 1
                else:
                    h = 0
                    print("Resting time")
                    time.sleep(self.rest_time)
                l += 1
            else:
                print("Follow limit reached")
                exit()
        #self.endTask(tid)
        print("Mass Follow completed")

    # Unfollow mass users
    def mass_unfollow(self, _list):
        h = 0
        l = 0
        task = 'mass-unfollow'
        tid = self.generateRandomId()
        _mx = len(_list)
        self.startTask(self.username, task, tid, _mx)
        for i in _list:
            if l < self.unfollow_limit:
                if h < self.limit:
                    self.unfollow_user(i)
                    self.updateTask(tid)
                    print(f'{i} unfollowed')
                    h = h + 1
                    time.sleep(self.normal_rest_time)
                else:
                    h = 0
                    print("Resting time")
                    time.sleep(self.rest_time)
                l += 1
            else:
                print("Unfollow limit reached")
                exit()
        self.save_unfollowed(_list)
        self.endTask(tid)
        print("Mass unfollow completed")

    def deletePosts(self):
        try:
            task = 'delete-posts'
            tid = self.generateRandomId()
            self.browser.find_elements_by_css_selector('.gKAyB')[3].click()
            print("profile")
            time.sleep(3)
            _max = self.delete_limit
            self.startTask(self.username, task, tid, _max)
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

    
    def doComment(self, purl, comment):
        try:
            self.browser.get(purl)
            time.sleep(self.rest)
            self.browser.find_elements_by_css_selector('.wpO6b')[1].click()
            # input = self.browser.find_element_by_css_selector('.X7cDz textarea')
            webdriver.ActionChains(self.browser).send_keys(comment).perform()
            time.sleep(1)
            self.browser.find_element_by_css_selector('.X7cDz button').click()
            time.sleep(self.rest)
        except NoSuchElementException:
            print('Element not found')

    def doComments(self, purl, comment):
        try:
            self.browser.get(purl)
            time.sleep(self.rest)
            cc = len(comment)
            cc -= 1
            i = 0
            while i < self.comment_limit:
                cmt = random.randint(0, cc)
                self.browser.find_elements_by_css_selector('.wpO6b')[1].click()
                # input = self.browser.find_element_by_css_selector('.X7cDz textarea')
                webdriver.ActionChains(self.browser).send_keys(comment[cmt]).perform()
                time.sleep(1)
                self.browser.find_element_by_css_selector('.X7cDz button').click()
                time.sleep(self.rest)
                i += 1
                print(f'{i} comment')
        except NoSuchElementException:
            print('Element not found')
        

    # Accept all requests
    def acceptRequest(self):
        try:
            task = 'accept-request'
            tid = self.generateRandomId()
            self.startTask(self.username, task, tid, self.download_limit)
            self.browser.get('https://www.instagram.com/')
            time.sleep(self.rest)
            self.close_notification_dialog()
            btn = self.browser.find_elements_by_css_selector('.Fifk5 a')
            btn[3].click()
            time.sleep(self.rest)
            open = self.browser.find_elements_by_css_selector('.PUHRj')
            open[0].click()
            btn = self.browser.find_elements_by_css_selector('.PUHRj .y3zKF')
            max_limit = len(btn)
            if max_limit > self.confirm_limit:
                max_limit = self.confirm_limit
            i = 0
            while i < max_limit:
                btn[i].click()
                i += 1
                print(f'{i} request confirmed')
                self.updateTask(tid)
            self.endTask(tid)
        except NoSuchElementException:
            print('Element not found')

    def download_post(self, username):
        try:
            task = 'download-post'
            tid = self.generateRandomId()
            self.startTask(self.username, task, tid, self.download_limit, username)
            self.browser.get('https://www.instagram.com/' + username + '/')
            time.sleep(self.rest)
            span = self.browser.find_elements_by_css_selector('.g47SY')
            post = int(span[0].text)
            max_limit = self.download_limit
            if max_limit > post:
                max_limit = post
            self.browser.find_elements_by_css_selector('div .eLAPa')[0].click()
            time.sleep(1)
            i = 0
            dl = []
            while i < max_limit:
                time.sleep(4)
                post = self.browser.find_elements_by_css_selector('.ZyFrc img')
                image = post[0].get_attribute('src')
                ui = self.generateRandomId()
                save = "cdn/public/download/post/" + username + "-" + ui +".jpg"
                urllib.request.urlretrieve(image, save)
                dl.append(save)
                post_next = self.browser.find_element_by_xpath('//a[contains(text(),\'Next\')]')
                post_next.click()
                time.sleep(self.rest)
                i = i + 1.
                print(f'{i} posts download')
                self.updateTask(tid)
            path = 'output/download/' + self.username + '.json'
            user = {'username': username, 'post': dl, 'tid': tid}
            with open(path, 'w', encoding='utf-8') as fi:
                json.dump(user, fi, ensure_ascii=False)
            self.endTask(tid)

        except NoSuchElementException:
            print('Element not found')


    def save_image(self, src, url):
        urllib.request.urlretrieve(src, url)

    def save_post_data(self, user, _m):
        dl = []
        _max = int(_m)
        path = '../../../../cdn/bot/public/download/post/' + self.username + '/' + user + '/'
        if _max > self.download_limit:
            _max = self.download_limit
        if not os.path.exists(path):
            os.makedirs(path)
        data = self.downloadPost(user, _max)
        with open('cache/download/post/'+user+'.json', 'w', encoding='utf-8') as fi:
            json.dump(data, fi, ensure_ascii=False)
        task = 'download-post'
        tid = self.generateRandomId()
        self.startTask(self.username, task, tid, _max, user)
        cou = 1
        for i in data:
            ui = self.generateRandomId()
            save = path + user + "-" + ui + "-" + self.username + ".jpg"
            self.save_image(i, save)
            dl.append(save)
            self.updateTask(tid)
            print(cou)
            cou = cou + 1
        path = 'cache/download/' + self.username + '.json'
        user = {'username': user, 'post': dl}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)
        self.endTask(tid)

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
                time.sleep(8)
                i = i + 1
                print(f'{i} story viewed')
                self.updateTask(tid)
            self.endTask(tid)
        except NoSuchElementException:
            print('Element not found')

    # Like posts from hastag
    def like_has(self, hastag):
        try:
            task = 'like-hastag'
            tid = self.generateRandomId()
            self.startTask(self.username, task, tid, self.like_limit, hastag)
            self.browser.get('https://www.instagram.com/explore/tags/' + hastag)
            time.sleep(self.rest)
            max_limit = self.like_limit
            self.browser.find_elements_by_css_selector('div .eLAPa')[0].click()
            time.sleep(1)
            i = 0
            while i < max_limit:
                btn = self.browser.find_element_by_css_selector('.fr66n button')
                btn.click()
                post_next = self.browser.find_element_by_xpath('//a[contains(text(),\'Next\')]')
                post_next.click()
                time.sleep(self.rest)
                i = i + 1
                print(f'{i} posts liked')
                self.updateTask(tid)
            self.endTask(tid)
        except NoSuchElementException:
            print('Element not found')

    # Like posts from hastag multiple
    def like_hastag(self, hastag):
        for un in hastag:
            self.like_has(un)

    # Send post as a direct message
    def send_post(self, user_list, link):
        task = 'message-send'
        tid = self.generateRandomId()
        _m = str(len(user_list))
        # self.startTask(self.username, task, tid, _m)
        self.browser.get(link)
        time.sleep(self.rest)
        self.close_notification_dialog()
        for ul in user_list:
            try:
                share_btns = self.browser.find_elements_by_css_selector('.wpO6b')
                share_btn = share_btns[2]
                share_btn.click()
                time.sleep(1)
                direct_btns = self.browser.find_element_by_xpath("//div[contains(text(),'Share to Direct')]")
                direct_btn = direct_btns
                direct_btn.click()
                time.sleep(2)
                msg_box = self.browser.find_elements_by_css_selector('input')[1]
                msg_box.send_keys(ul)
                time.sleep(self.rest)
                select_btns = self.browser.find_elements_by_css_selector('.dCJp8')
                select_btn = select_btns[0]
                select_btn.click()
                send_btn = self.browser.find_element_by_xpath("//button[contains(text(),'Send')]")
                send_btn.click()
                time.sleep(2)
                # self.updateTask(tid)
            except NoSuchElementException:
                print("Element not found")
        # self.endTask(tid)

    # Send a direct message
    def send_message(self, user_list, msg):
        for ul in user_list:
            task = 'message-direct'
            tid = self.generateRandomId()
            self.startTask(self.username, task, tid, len(user_list))
            self.browser.get('https://www.instagram.com/direct/new/')
            time.sleep(self.rest)
            self.close_notification_dialog()
            username_boxs = self.browser.find_elements_by_css_selector('input')
            username_box = username_boxs[1]
            username_box.send_keys(ul)
            time.sleep(self.rest)
            select_btns = self.browser.find_elements_by_css_selector('.dCJp8')
            select_btn = select_btns[0]
            select_btn.click()
            next_btn = self.browser.find_elements_by_css_selector('button')
            next_btn[4].click()
            time.sleep(self.rest)
            self.browser.find_element_by_css_selector('textarea').send_keys(msg)
            send_btn = self.browser.find_elements_by_css_selector('button')
            send_btn[6].click()
            print('ul')
            self.updateTask(tid)
            time.sleep(2)
        self.endTask(tid)

    def send_messages(self, user, msg, _loop):
        self.browser.get('https://www.instagram.com/direct/new/')
        time.sleep(self.rest)
        self.close_notification_dialog()
        username_boxs = self.browser.find_elements_by_css_selector('input')
        username_box = username_boxs[1]
        username_box.send_keys(user)
        time.sleep(self.rest)
        select_btns = self.browser.find_elements_by_css_selector('.dCJp8')
        select_btn = select_btns[0]
        select_btn.click()
        next_btn = self.browser.find_element_by_xpath("//button[contains(text(),'Next')]")
        next_btn.click()
        time.sleep(self.rest)
        l = 0
        while l < _loop: 
            self.browser.find_element_by_css_selector('textarea').send_keys(msg)
            send_btn = self.browser.find_element_by_xpath('//button[text() = "Send"]')
            send_btn.click()
            l += 1

     # Retrive user's following list
    def unfollowFast(self):
        try:
            following = []
            self.browser.get('https://www.instagram.com/' + self.username)
            max_limit = self.unfollow_limit
            following_link = self.browser.find_elements_by_css_selector('ul li a')
            following_link[1].click()
            time.sleep(self.rest)
            dialog = self.browser.find_element_by_css_selector('div[role=\'dialog\']')
            following_list = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
            number_of_following_in_list = len(following_list.find_elements_by_css_selector('li'))
            action_chain = webdriver.ActionChains(self.browser)

            while number_of_following_in_list < max_limit:
                dialog.click()
                action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                number_of_following_in_list = len(following_list.find_elements_by_css_selector('li'))
                print(number_of_following_in_list)

            time.sleep(1)
            i = 0
            li = following_list.find_elements_by_css_selector('li')
            lt = 0
            while lt < max_limit:
                print(lt)
                li[lt].find_element_by_xpath('//button[text() = "Following"]').click()
                self.browser.find_element_by_xpath('//button[text() = "Unfollow"]').click()
                time.sleep(2)
                i += 1
                lt += 1

                if i > 20:
                    print('resting time')
                    time.sleep(20)
                    i = 0
            '''
            for user in following_list.find_elements_by_css_selector('li'):
                user_link = user.find_element_by_css_selector('a').get_attribute('href')
                user_name = user_link.replace('https://www.instagram.com/', '')
                user_name = user_name.replace('/', '')
                print(user_name)
                following.append(user_name)
                user.find_element_by_xpath('//button[text() = "Following"]').click()
                time.sleep(1)
                self.browser.find_element_by_xpath('//button[text() = "Unfollow"]').click()
                time.sleep(4)
                i += 1

                if i > 20:
                    print('resting time')
                    time.sleep(20)
                    i = 0

                if len(following) == max_limit:
                    break
            '''

        except NoSuchElementException:
            print('Element not found')

    # Retrive user's following list
    def get_user_following(self, username):
        try:
            following = []
            self.browser.get('https://www.instagram.com/' + username)
            time.sleep(self.rest)
            count = self.browser.find_elements_by_class_name("g47SY")[2].text
            count = count.replace(',', '')
            count = count.replace('.', '')
            count = count.replace('k', '')
            count = count.replace('m', '')
            max_limit = int(count)
            print(max_limit)

            if max_limit == 0:
                return following

            if self.list_following_limit < max_limit:
                max_limit = self.list_following_limit

            print("max")
            print(max_limit)

            following_link = self.browser.find_elements_by_css_selector('ul li a')
            following_link[1].click()
            time.sleep(self.rest)
            dialog = self.browser.find_element_by_css_selector('div[role=\'dialog\']')
            following_list = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
            number_of_following_in_list = len(following_list.find_elements_by_css_selector('li'))
            print(number_of_following_in_list)
            action_chain = webdriver.ActionChains(self.browser)
            while number_of_following_in_list < max_limit:
                dialog.click()
                action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                number_of_following_in_list = len(following_list.find_elements_by_css_selector('li'))
                print(number_of_following_in_list)
            time.sleep(1)

            for user in following_list.find_elements_by_css_selector('li'):
                user_link = user.find_element_by_css_selector('a').get_attribute('href')
                user_name = user_link.replace('https://www.instagram.com/', '')
                user_name = user_name.replace('/', '')
                print(user_name)
                following.append(user_name)
                user_dp = user.find_element_by_css_selector('img').get_attribute('src')
                self.saveDp(user_name, user_dp)
                self.addInstagramUser(username, user_name, 'following', 'scrape')
                if len(following) == max_limit:
                    break

            return following

        except NoSuchElementException:
            print('Element not found')


    # Retrive user's followers list
    def get_user_followers(self, username):
        try:
            self.browser.get('https://www.instagram.com/' + username)
            time.sleep(self.rest)

            followers_count = self.browser.find_elements_by_class_name("g47SY")
            count = followers_count[1].text
            count = count.replace(',', '')
            count = count.replace('.', '')
            count = count.replace('k', '')
            count = count.replace('m', '')
            max_limit = int(count)
            print(max_limit)

            followers = []

            if max_limit == 0:
                return followers

            if self.list_follower_limit < max_limit:
                max_limit = self.list_follower_limit

            print("max")
            print(max_limit)

            followers_link = self.browser.find_element_by_css_selector('ul li a')
            followers_link.click()
            time.sleep(3)
            dialog = self.browser.find_element_by_css_selector('div[role=\'dialog\']')
            followers_list = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
            number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))
            print("no of followers")
            print(number_of_followers_in_list)
            action_chain = webdriver.ActionChains(self.browser)

            while number_of_followers_in_list < max_limit:
                dialog.click()
                action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))
                print(number_of_followers_in_list)

            for user in followers_list.find_elements_by_css_selector('li'):
                user_link = user.find_element_by_css_selector('a').get_attribute('href')
                user_name = user_link.replace('https://www.instagram.com/', '')
                user_name = user_name.replace('/', '')
                print(user_name)
                followers.append(user_name)
                user_dp = user.find_element_by_css_selector('img').get_attribute('src')
                self.saveDp(user_name, user_dp)
                self.addInstagramUser(username, user_name, 'follower', 'scrape')
                if len(followers) == max_limit:
                    break

            return followers

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
        path = 'cache/output/' + self.username + '-unfollowed.json'
        user = {'username': self.username, 'unfollowed': _list}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)
    
    def save_ghost(self, _list):
        path = 'cache/output/' + self.username + '-ghost.json'
        user = {'username': self.username, 'ghost': _list}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    # Save JSON file with user details like followers and following data
    def save_file(self, followers, followings, username):
        path = 'cache/output/' + username + '.json'
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
        path = 'cache/output/' + username + '-none.json'
        user = {'none': c}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    def save_none_following(self, username):
        c = self.get_none_following(username)
        path = 'cache/output/' + username + '-fan.json'
        user = {'fan': c}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    def save_common_followers(self, username):
        c = self.get_common_followers(username)
        path = 'cache/output/' + username + '-common.json'
        user = {'common': c}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)

    # Get followers data from the JSON file
    def read_followers(self, username):
        path = 'cache/output/' + username + '.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                user_file = json.load(f)
                user_followers = user_file['followers']
                f.close()
                # print(user_followers)
        except IOError:
            print('File not found on local disk fetching from server')
            user_followers = self.get_user_followers(username)
        return user_followers

    # Get following data from JSON file
    def read_following(self, username):
        path = 'cache/output/' + username + '.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                user_file = json.load(f)
                user_following = user_file['following']
                f.close()
                # print(user_following)
        except IOError:
            print('File not found on local disk fetching from server')
            user_following = self.get_user_following(username)
        return user_following

    # Get user list who not follow back you
    def read_none_followers(self, username):
        path = 'cache/output/' + username + '-none.json'
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
        path = 'cache/output/' + username + '-fan.json'
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
        path = 'cache/output/' + username + '-common.json'
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

    def downloadPost(self, user, _max=30):
        path = "cache/session/" + self.username + "/"
        self.ig.with_credentials(self.username, self.password, path)
        post = []
        medias = self.ig.get_medias(user, _max)
        for m in medias:
            post.append(m.image_high_resolution_url)
        return post

    def getHastag(self, has, _max=10): 
        _m = _max
        medias = self.ig.get_medias_by_tag(has, _m)
        return medias

    def getMediaByUrl(self, _url):
        m = self.ig.get_media_by_url(_url)
        return m
        
    def getMediaId(self, _url):
        m = self.getMediaByUrl(_url)
        i = m.identifier
        return i
        
    def likeMediaById(self, _id):
        self.userLogin()
        self.ig.like(_id)

    def downloadHastagImage(self, has, _max=50):
        post = []
        if _max > self.download_limit:
            _max = self.download_limit
        medias = self.getHastag(has, _max)
        for m in medias:
            post.append(m.image_high_resolution_url)
        dl = []
        path = 'cdn/public/download/post/' + self.username + '/#' + has + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        task = 'download-post'
        tid = self.generateRandomId()
        self.startTask(self.username, task, tid, _max, '#' + has)
        for i in post:
            ui = self.generateRandomId()
            save = path + has + "-" + ui + "-" + self.username + ".jpg"
            self.save_image(i, save)
            dl.append(save)
            self.updateTask(tid)
        path = 'output/download/' + self.username + '.json'
        user = {'username': self.username, 'post': dl}
        with open(path, 'w', encoding='utf-8') as fi:
            json.dump(user, fi, ensure_ascii=False)
        self.endTask(tid)
        

    def likeHastag(self, has, _max=10):
        self.userLogin()
        i = 0
        _m = self.like_limit
        h = self.getHastag(has)
        for m in h:
            if i < _m:
                self.ig.like(m.identifier)
            else:
                print('Like limit reached')
            i += 1

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

    def unfollowNoneFast(self):
        _list = self.read_none_followers(self.username)
        self.userLogin()
        for l in _list:
            _info = self.ig.get_account(l)
            self.ig.unfollow(_info.identifier)
            print(_info.username + " unfollowed")
