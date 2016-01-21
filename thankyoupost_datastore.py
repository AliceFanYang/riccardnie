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

    # @classmethod
    # def GetUserLikes(cls, key):
    #     key = ndb.Key(urlsafe = key)
    #     entry = key.get()
    #     if entry:
    #         return entry.user_likes

# This is the handler to load an image stored in a Review entity.
# The request comes as /getimg/<entity_key>, and is separated by means of
# regular expressions grouping in the "app" component at the end of this file.
# The <entity_key> is passed in as an argument, since we used grouping in the
# definition of app.
# class ViewPhotoHandler(webapp2.RequestHandler):
#     def get(self, review_key):
#         # Step 1: let's get the entity.
#         review_normalized_key = ndb.Key(urlsafe=review_key)
#         review = review_normalized_key.get()
#         # Step 2: if the entity has an image, send it.
#         if hasattr(review, 'image'):
#             # We must specify the type of file we are sending. In this app,
#             # for simplicity, we will assume only png, but we could have stored
#             # info on the file type in a separate property in Datastore, to be
#             # more flexible.
#             self.response.headers['Content-Type'] = 'image/png'
#             self.response.write(review.image)

# Handler that will take care of receiving and saving a new review
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

        # place_name = self.request.get('place_name')
        # category = self.request.get('category')
        # description = self.request.get('description')
        # review_img_link = self.request.get('review_img_link')
        # image = None
        # if self.request.get('review_img'):
        #     image = self.request.get('review_img')
        # amenities = []
        # # Let's find all the attributes whose key looks like "amenities-.*"
        # for key,value in self.request.POST.items():
        #     re_obj = re.search(r'^amenity-(.*)',key)
        #     if re_obj and value == "on":
        #         amenities.append(str(re_obj.group(0)))
        # First thing for a new review should be check for duplicates
        # We will check for Restaurant AND Category, so that two places with the
        # same name but belonging to different categories can be safely stored.
        # This is the kind of behavior that we would want to test with a unit
        # test.
        if post_title and message:
            #search_review = Review.query(Review.title == place_name, Review.category == category)
            #results = search_review.fetch()
            #if results:
            #    logging.warning("We have already an entry of type %s named %s. Skipping." % (category, place_name))
            #else:
            new_thankyou = ThankYou(
                title = post_title,
                name = person_name,
                icon_link = icon_img_link,
                message = message,
                present_riccardo = riccardo_img_link,
                present_riccardo_caption = riccardo_caption,
                present_sidnie = sidnie_img_link,
                present_sidnie_caption = sidnie_caption
                # title = place_name,
                # # description = description,
                # category = category,
                # # can be empty
                # image_link = review_img_link,
                # image = image,
                # user_likes = 1,
                # amenities = amenities
            )
            new_thankyou.put()
        else:
            # This should also be validated in the client before sending the request.
            logging.warning("Ignoring request because it has no post title or body")
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/save-post', SavePostHandler),
    # Anything that looks like /getimg/<something> will be accepted.
    # /getimg/ with nothing attached will not since it has nothing after getimg/
    # ('/getimg/(.+)', ViewPhotoHandler),
], debug=True)
