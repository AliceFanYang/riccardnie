#!/usr/bin/env python
import webapp2

from google.appengine.api import users
import logging
import os
import jinja2
import logging

import thankyoupost_datastore as ty_ds

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Sends to the browser a form to create new reviews.
class ThankYouFormHandler(webapp2.RequestHandler):
    def get(self):
        # user = users.get_current_user()
        # if user:
        template_header = JINJA_ENVIRONMENT.get_template('templates/header.html')
        template_footer = JINJA_ENVIRONMENT.get_template('templates/footer.html')
                # Start by writing the header
        header_values = {}
        header_values["menu_entry_1"] = "List All Entries"
        header_values["menu_entry_1_link"] = "/"
        # header_values["logout_link"] = users.create_logout_url('/')

        self.response.write(template_header.render(header_values))
        # Fill the body
        # template_values = {'username': user.nickname(),
        #                    'logout_link': users.create_logout_url('/')}
        template = JINJA_ENVIRONMENT.get_template('templates/thankyou_form.html')
        self.response.write(template.render())#template_values))
        # Close the page
        self.response.write(template_footer.render())
        # else:
        #     # if the user is not logged in, let's have them log in.
        #     self.redirect(users.create_login_url('/create_review'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template_header = JINJA_ENVIRONMENT.get_template('templates/header.html')
        template_footer = JINJA_ENVIRONMENT.get_template('templates/footer.html')
        # Start by writing the header
        header_values = {}
        header_values["menu_entry_1"] = "Submit New Thank You"
        header_values["menu_entry_1_link"] = "/create-thankyou"
        # if user:
        #     header_values["logout_link"] = users.create_logout_url('/')
        # else:
        #     header_values["login_link"] = users.create_login_url('/')

        self.response.write(template_header.render(header_values))
        # Fill the body
        template_values ={}
        template_values['entries'] = []
        entries = ty_ds.Review.query().fetch()
        for entry in entries:
            new_entry = {
                "title": entry.title,
                "name": entry.name,
                "message": entry.message,
                "present_riccardo_caption": entry.present_riccardo_caption,
                "present_sidnie_caption": entry.present_sidnie_caption
            }

            #icon_link
            #present_riccardo
            #present_sidnie

            # new_entry['name'] = entry.title
            # new_entry['category'] = entry.category
            # new_entry['description'] =  entry.description
            # new_entry['amenities'] =  entry.amenities
            # new_entry['user_likes'] = entry.user_likes
            # we use this check to avoid potential errors if the element was
            # not entered. Ideally, we should check every element if we know
            # that it is required. Both in the F-E before sending the form, and
            # here in the B-E before processing the request.

            # if (hasattr(entry, 'image') and entry.image != None):
            #     # creates a new link that can be used to retrieve the specific
            #     # image associated to this entity.
            #     new_entry['imglink'] = '/getimg/%s' % entry.key.urlsafe()
            if hasattr(entry, "icon_link"):
                new_entry["icon_link"] = entry.icon_link
            if hasattr(entry, "present_riccardo"):
                new_entry["present_riccardo"] = entry.present_riccardo
            if hasattr(entry, "present_sidnie"):
                new_entry["present_sidnie"] = entry.present_sidnie

            new_entry['entry_id'] = entry.key.urlsafe()
            template_values['entries'].append(new_entry)

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))
        # Close the page
        self.response.write(template_footer.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create-thankyou', ThankYouFormHandler),
], debug=True)
