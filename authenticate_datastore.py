#!/usr/bin/env python
import webapp2
import logging
from google.appengine.ext import ndb
import re

class AuthenticateUsers(ndb.Model):
    # Person's email
    email = ndb.StringProperty(required = True)

class SaveUserHandler(webapp2.RequestHandler):
    def post(self):
        user_email = self.request.get("user_email")

        if email:
            new_entry = AuthenticateUsers(
                email = user_email
            )
            new_entry.put()
        else:
            logging.warning("Ignoring request because it has no email")
        self.redirect("/")

class CreateAcceptedUsers(webapp2.RequestHandler):
    def get(self):
        email_list = [ # list of accepted users
        ]
        if len(AuthenticateUsers.query().fetch()) == 0:
            for user_email in email_list:
                AuthenticateUsers(email = user_email).put()

app = webapp2.WSGIApplication([
    ("/create-users", CreateAcceptedUsers)
], debug=True)
