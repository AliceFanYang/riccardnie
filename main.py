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
        template_header = JINJA_ENVIRONMENT.get_template('templates/header.html')
        template_footer = JINJA_ENVIRONMENT.get_template('templates/footer.html')

        header_values = {}
        header_values["menu_entry_1"] = "List All Entries"
        header_values["menu_entry_1_link"] = "/"

        self.response.write(template_header.render(header_values))
        # Fill the body
        # template_values = {'username': user.nickname(),
        #                    'logout_link': users.create_logout_url('/')}
        template = JINJA_ENVIRONMENT.get_template('templates/thankyou_form.html')
        self.response.write(template.render())#template_values))
        # Close the page
        self.response.write(template_footer.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template_header = JINJA_ENVIRONMENT.get_template('templates/header.html')
        template_footer = JINJA_ENVIRONMENT.get_template('templates/footer.html')
        # Start by writing the header
        header_values = {}
        header_values["menu_entry_1"] = "Submit New Thank You"
        header_values["menu_entry_1_link"] = "/create-thankyou"

        self.response.write(template_header.render(header_values))
        # Fill the body
        template_values ={}
        template_values['entries'] = []
        entries = ty_ds.ThankYou.query().fetch()
        for entry in entries:
            new_entry = {
                "title": entry.title,
                "name": entry.name,
                "message": entry.message,
                "present_riccardo_caption": entry.present_riccardo_caption,
                "present_sidnie_caption": entry.present_sidnie_caption
            }

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
