# -*- coding: utf-8 -*-
from data_parser.models import PostData, ParseError

import requests
from bs4 import BeautifulSoup
from threading import Thread, Lock
import time


def get_category():
  res = requests.get("https://www.dcard.tw/f", headers = { 'Connection':'close' })
  soup = BeautifulSoup(res.text, 'html.parser')
  target_tag = soup.find_all('a', class_ = "ForumEntry_link_3tNC4")

  category_list = []
  for i in target_tag:
    category_list.append(i["href"].split("/")[-1])

  category_list.remove('f')

  return category_list

def parse_id(category):

  id_loop = ""

  s = requests.Session()
  s.keep_alive = False

  while True:
    print id_loop

    try:
      res = s.get("https://www.dcard.tw/_api/forums/"+ category +"/posts?popular=false" + str(id_loop))

      print res.status_code

      id_loop = "&before=" + str(res.json()[-1]["id"])      

    except Exception,e:

      print str(e)

      if str(e) == "list index out of range":
        break
      else:
        print "幹幹幹幹幹幹幹幹幹幹幹幹幹幹幹幹幹幹幹幹"
        time.sleep(10)
        continue
    
    #create row data
    for post in res.json():
      try:

        if post["anonymousSchool"]:
          PostData.objects.update_or_create(
            id = post["id"],
            defaults = {
            'title': post["title"],
            'gender': post["gender"],
            'like_count': post["likeCount"],
            'comment_count': post["commentCount"],
            'created_at': post["createdAt"],
            'forum_alias': post["forumAlias"],
            'forum_name': post["forumName"],
            'school_name': "anonymous"
          })
        else:
          PostData.objects.update_or_create(
            id = post["id"],
            defaults = {
            'title': post["title"],
            'gender': post["gender"],
            'like_count': post["likeCount"],
            'comment_count': post["commentCount"],
            'created_at': post["createdAt"],
            'forum_alias': post["forumAlias"],
            'forum_name': post["forumName"],
            'school_name': post["school"]
          })

      except Exception,e:

        print str(e)
        continue 

def start_parse_post():
  category_list = get_category()
  
  workers = []

  for i in category_list:
    
    worker = Thread(target = parse_id, args = (i, ))
    workers.append(worker)
    worker.start()
    
  for worker in workers:
    worker.join()






