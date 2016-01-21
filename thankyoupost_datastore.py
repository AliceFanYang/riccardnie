#!/usr/bin/env python
import webapp2
import logging
from google.appengine.ext import ndb
import re

class ThankYou(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    # Title of the post
    title = ndb.StringProperty(required = True)
    # Person's name
    name = ndb.StringProperty(required = True)
    # Link to the person's icon
    icon_link = ndb.StringProperty()
    # Message of the post
    message = ndb.TextProperty(indexed = False, required = True)
    # Link to picture for Riccardo's present
    present_riccardo = ndb.StringProperty()
    # Caption for Riccardo's present
    present_riccardo_caption = ndb.StringProperty()
    # Link to picture for Sidnie's present
    present_sidnie = ndb.StringProperty()
    # Caption for Sidnie's present_sidnie
    present_sidnie_caption = ndb.StringProperty()

# Handler that will take care of receiving and saving a new post
class SavePostHandler(webapp2.RequestHandler):
    # The advantage of a post handler for the form is that we can upload
    # arbitrarily large chunks of information, such as images.
    def post(self):
        post_title        = self.request.get("post_title")
        person_name       = self.request.get("person_name")
        icon_img_link     = self.request.get("icon_img_link")
        message           = self.request.get("message")
        riccardo_img_link = self.request.get("riccardo_img_link")
        riccardo_caption  = self.request.get("riccardo_caption")
        sidnie_img_link   = self.request.get("sidnie_img_link")
        sidnie_caption    = self.request.get("sidnie_caption")

        if post_title and message: # must have
            new_thankyou = ThankYou(
                title = post_title,
                name = person_name,
                icon_link = icon_img_link,
                message = message,
                present_riccardo = riccardo_img_link,
                present_riccardo_caption = riccardo_caption,
                present_sidnie = sidnie_img_link,
                present_sidnie_caption = sidnie_caption
            )
            new_thankyou.put()
        else:
            # This should also be validated in the client before sending the request.
            logging.warning("Ignoring request because it has no post title or body")
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/save-post', SavePostHandler),
], debug=True)
