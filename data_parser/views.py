# -*- coding: utf-8 -*-
from django.shortcuts import render
from data_parser.models import PostData, ParseError
from django.shortcuts import  render_to_response
from django.template import RequestContext

from parser_method.testt import testt

import requests
from bs4 import BeautifulSoup
import random
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


def parse_content_func(category):

  print category
  
  for post in PostData.objects.filter(forum_alias = category):
    res = requests.get("https://www.dcard.tw/_api/posts/"+ str(post.id), headers = { 'Connection':'close' }).json()

    post.like_count = res["likeCount"]
    post.comment_count = res["commentCount"]
    post.content = res["content"]

    print str(post.id) + "parse content"

    post.save()


def parse_content(category_list):

  content_workers = []
  for category in category_list[0:32]:
    worker = Thread(target = parse_content_func, args = (category, ))
    content_workers.append(worker)
    worker.start()

  for worker in content_workers:
    worker.join()

  
def parse_content_data(category):
  for post in PostData.objects.filter(forum_alias = category):

    time.sleep(0.5)
    print post.id

    try:
      res = requests.get("https://www.dcard.tw/_api/posts/" + str(post.id), headers = { 'Connection':'close' }).json()

      try:
        post.content = res["content"]
      except:
        post.content = "post no found"

      if res["anonymousSchool"]:
        post.school_name = "anonymous"
      else:
        post.school_name = res["school"]

    except Exception,e:
      print str(e)

      continue

    post.save()  

def index(request):
  category_list = get_category()
  
  workers = []

  tStart = time.time()

  for i in category_list:
    
    worker = Thread(target = parse_id, args = (i, ))
    workers.append(worker)
    worker.start()
    
  for worker in workers:
    worker.join()
  
  # parse_content(category_list)

  tEnd = time.time()
  spent_time = tEnd - tStart

  return render_to_response('index.html',RequestContext(request,locals()))


def parse_content(request):
  category_list = get_category()

  print "all category"
  print category_list

  # category_list = reversed(category_list)

  workers = []

  for category in category_list[0:32]:
    worker = Thread(target = parse_content_data, args = (category, ))
    workers.append(worker)
    worker.start()

  for worker in workers:
    worker.join()

  return render_to_response('index.html',RequestContext(request,locals()))


def test(request):

  print testt(1)

  return render_to_response('index.html',RequestContext(request,locals()))












