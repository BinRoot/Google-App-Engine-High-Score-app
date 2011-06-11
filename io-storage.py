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
import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class HighScore(db.Model):
    username = db.StringProperty(multiline=False)
    score = db.StringProperty(multiline=False)

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    highscores = db.GqlQuery("SELECT * "
                             "FROM HighScore")

    for sc in highscores:
      self.response.out.write(cgi.escape(sc.username)+':'+cgi.escape(sc.score+';'))
    
    self.response.out.write("""
          <form action="/sign" method="post">
            <div><textarea name="content" rows="1" cols="30"></textarea></div>
            <div><textarea name="score" rows="1" cols="10"></textarea></div>
            <div><input type="submit" value="Update"></div>
          </form>
        </body>
      </html>""")

class Guestbook(webapp.RequestHandler):
  def post(self):
    sc = HighScore()
    sc.username = self.request.get('content')
    sc.score = self.request.get('score')
    sc.put()
    self.redirect('/')


application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/sign', Guestbook)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
