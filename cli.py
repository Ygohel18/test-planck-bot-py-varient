#!/bin/bash
import time
import bot
import sys
import mobile

username = sys.argv[1]
password = sys.argv[2]
action = sys.argv[3]
user = ''

def setup(username, password):
    b = bot.Bot(username, password)
    #b.loginAdmin()
    b.login()
    time.sleep(b.rest)
    b.close_notification_dialog()
    time.sleep(b.rest)
    return b

def direct(username, password):
    b = bot.Bot(username, password, False)
    time.sleep(b.rest)
    return b

def m(username, password):
    b = mobile.Bot(username, password)
    b.login()
    time.sleep(b.rest)
    b.close_notification_dialog()
    time.sleep(6)
    b.close_notification_dialog2()
    time.sleep(b.rest)
    return b

if action == "help":
    with open('./README.txt') as f:
        help = f.read()
        print(help)

if action == "saveuser":
    user = sys.argv[4]
    b = setup(username, password)
    #b = direct(username, password)
    follower = b.get_user_followers(user)
    following = b.get_user_following(user)
    b.save_file(following, following, user)

if action == "loginig":
    b = direct(username, password)
    b.userLogin()

if action == "updateuserdata":
    b = direct(username, password)
    b.updateUserData()
    #b.saveFile(username)

if action == "savenone":
    user = sys.argv[4]
    b = setup(username, password)
    b.save_none_followers(user)
    print("File saved")
    b.close_browser()
    
if action == "likehastag":
    hastag = sys.argv[4]
    b = setup(username, password)
    h = hastag.split(' ')
    for i in h:
        b.like_has(i)
    print("Liked success")
    b.close_browser()

if action == "viewhastagstory":
    hastag = sys.argv[4]
    b = setup(username, password)
    h = hastag.split(' ')
    for i in h:
        b.viewStory(i)
    print("Seen success")
    b.close_browser()

if action == "request":
    b = setup(username, password)
    b.acceptRequest()
    print("Accept success")
    b.close_browser()

if action == "delete":
    b = m(username, password)
    b.deletePosts()
    print("Accept success")
    b.close_browser()

if action == "massfollow":
    user = sys.argv[4]
    b = setup(username, password)
    type = sys.argv[5]
    if type == "follower":
        # list = b.read_followers(user)
        list = b.getUserFollowers(user)
    if type == "following":
        # list = b.read_following(user)
        list = b.getUserFollowing(user)
    if type == "fan":
        list = b.read_none_following(user)
    if type == "common":
        list = b.read_common_followers(user)
    if type == "none":
        list = b.read_none_followers(user)
    b.mass_follow(list)
    b.close_browser()

if action == "massunfollow":
    b = setup(username, password)
    type = sys.argv[4]
    if type == "all":
        list = b.read_following(username)
    if type == "none":
        list = b.read_none_followers(username)
    if type == "common":
        list = b.read_common_followers(username)
    b.mass_unfollow(list)
    b.close_browser()

if action == "unfollowfast":
    b = setup(username, password)
    b.unfollowFast()
    b.close_browser()

if action == "dluser":
    user = sys.argv[4]
    b = direct(username, password)
    type = sys.argv[5]
    _max = sys.argv[6]
    if type == "post":
        b.save_post_data(user, _max)
    if type == "story":
        print('Soon')
    if type == "dp":
        print('Soon')
	
if action == "message":
    message = sys.argv[4]
    user = sys.argv[5]
    to = sys.argv[6]
    type = sys.argv[7]
    b = setup(username, password)
    if to == "follower":
        list = b.read_followers(user)
    if to == "following":
        list = b.read_following(user)
    if type == "direct":
        b.send_message(list, message)
    else:
        b.send_post(list, message)
    b.close_browser()

	


