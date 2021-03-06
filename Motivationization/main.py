#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

import json
import random
import logging
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.api import users

from google.appengine.api import mail


jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Profile(ndb.Model):
    email = ndb.StringProperty(required=True)
    post_keys = []
    post_keys = ndb.KeyProperty(repeated=True)
    feelings = ndb.BlobProperty(indexed=True)
    favorite = ndb.StringProperty(repeated=True)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

gif_url = ""

# Define a Post model for the Datastore
class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    comment_keys = []
    comment_keys = ndb.KeyProperty(repeated=True)

class Comment(ndb.Model):
    # Your code goes here
    name = ndb.StringProperty(required=True)
    comment = ndb.TextProperty(required=True)
    datetime = ndb.DateTimeProperty(auto_now_add=True)

def GetProfile():
    user = users.get_current_user()
    current_profile = Profile.get_by_id(user.user_id())
    if current_profile == None:
        current_profile = Profile(email = user.nickname(), id = user.user_id())
        current_profile.put()
    return current_profile

class MainHandler(webapp2.RequestHandler):
    def get(self):
        GetProfile()
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.user_id(), users.create_logout_url('/')))
            template = jinja_environment.get_template('templates/main.html')
            self.response.out.write(template.render({"user": user.nickname(), "signout": users.create_logout_url('/')}))

#things22

class SallyHandler(webapp2.RequestHandler):
    def get(self):
        # Get all of the student data from the datastore
        '''     query_user = User.query(User.email == users.get_current_user().email())
        user_data = query_user.fetch()'''

        query = Post.query()
        post_data = query.fetch()
        # Pass the data to the template
        template_values = {
            'posts' : post_data,
            #'user' : user_data
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/asksally.html')
        self.response.write(template.render(template_values))

    def post(self):
        # Get the post title and content from the form
        title = self.request.get('title')
        content = self.request.get('content')
        # Create a new Student and put it in the datastore
        post = Post(title=title, content=content)
        post_key = post.put()
        # Attach the post to the user

        # Redirect to the main handler that will render the template
        self.redirect('/asksally')

class CommentHandler(webapp2.RequestHandler):
    def post(self):
        # Create the comment in the Database
        # !!!! YOUR CODE HERE
        comment = Comment(name = self.request.get('name2'), comment = self.request.get('comment'))
        comment_key = comment.put()
        # Find the post that was commented on using the hidden post_url_key
        post_url_key = self.request.get('post_url_key')
        post_key = ndb.Key(urlsafe=post_url_key)
        post = post_key.get()
        # Attach the comment to that post
        # !!!! YOUR CODE HERE
        post.comment_keys.append(comment_key)
        post.put()
        self.redirect('/asksally')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('displaying profile page')
        template = jinja_environment.get_template('templates/profile.html')
        current_profile = GetProfile()
        url = self.request.get('id')
        if url != "":
            if url not in current_profile.favorite:
                current_profile.favorite.append(url)
                current_profile.put()
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('/templates/profile.html')
        self.response.write(template.render(
        {"user": user.nickname(),
         'images' : current_profile.favorite,
         "signout": users.create_logout_url('/')}))

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        current_profile= GetProfile()
        index =int(self.request.get('index'))
        logging.info('deleting item %s', index)
        current_profile.favorite.pop(index)
        current_profile.put()
        self.redirect("/profile")

class QuestHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/templates/question.html')
        self.response.write(template.render({"signout": users.create_logout_url('/')}))

class LGifHandler(webapp2.RequestHandler):
    def get(self):
        base_url = 'http://api.giphy.com/v1/gifs/search?q='
        api_key_url = '&api_key=dc6zaTOxFJmzC&limit=40'
        search_term = 'hilarious'
        giphy_data_source = urlfetch.fetch(base_url + search_term + api_key_url)
        giphy_json_content = giphy_data_source.content
        parsed_giphy_dictionary = json.loads(giphy_json_content)
        rand_num = random.randint(0,39)
        gif_url= parsed_giphy_dictionary['data'][rand_num]['images']['original']['url']
        template = jinja_environment.get_template('templates/laughs.html')
        self.response.out.write(template.render({'results': gif_url, "signout": users.create_logout_url('/')}))

class MGifHandler(webapp2.RequestHandler):
    def get(self):
        base_url = 'http://api.giphy.com/v1/gifs/search?q='
        api_key_url = '&api_key=dc6zaTOxFJmzC&limit=40'
        search_term = 'motivation'
        giphy_data_source = urlfetch.fetch(base_url + search_term + api_key_url)
        giphy_json_content = giphy_data_source.content
        parsed_giphy_dictionary = json.loads(giphy_json_content)
        rand_num = random.randint(0,39)
        gif_url= parsed_giphy_dictionary['data'][rand_num]['images']['original']['url']
        template = jinja_environment.get_template('templates/motivation.html')
        self.response.out.write(template.render({'results': gif_url, "signout": users.create_logout_url('/')}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/comment', CommentHandler),
    ('/asksally', SallyHandler),
    ('/profile', ProfileHandler),
    ('/aboutus', QuestHandler),
    ('/laughs', LGifHandler),
    ('/motivation', MGifHandler),
    ('/delete', DeleteHandler)
], debug=True)
