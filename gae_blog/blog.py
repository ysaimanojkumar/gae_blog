# this is the main entry point for the application

import os
import sys

import webapp2

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from gae_blog.controllers import admin, author, contact, error, feed, \
    index, pingback, post, tag, trackback, verify, webmention

# url routes

ROUTES = [('/?', index.IndexController),
           ('/feed/?', feed.FeedController),
           ('/contact/?', contact.ContactController),
           ('/post/(.[^/]+)/?', post.PostController),
           ('/tag/(.[^/]+)/?', tag.TagController),
           ('/author/(.[^/]+)/?', author.AuthorController),
           ('/trackback/(.[^/]+)/?', trackback.TrackbackController),
           ('/pingback/?', pingback.PingbackController),
           ('/webmention/?', webmention.WebmentionController),
           ('/verify/?', verify.VerifyController),
           ('/admin/?', admin.AdminController),
           ('/admin/blog/?', admin.BlogController),
           ('/admin/author/(.*)/?', admin.AuthorController),
           ('/admin/authors/?', admin.AuthorsController),
           ('/admin/post/(.*)/?', admin.PostController),
           ('/admin/posts/?', admin.PostsController),
           ('/admin/preview/(.[^/]+)/?', admin.PreviewController),
           ('/admin/comments/?', admin.CommentsController),
           ('/admin/image/?', admin.ImageController),
           ('/admin/images/?', admin.ImagesController),
           ('/admin/migrate/?', admin.MigrateController),
           ('/(.*)', error.ErrorController)]

# any extra config needed when the app starts
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'replace this with the output from os.urandom(64)',
    'cookie_args': {
        # uncomment this line to force cookies to only be sent over SSL
        #'secure': True,

        # this can prevent XSS attacks by not letting javascript access the cookie
        # (note that some older browsers do not have this restriction implemented)
        # disable if you need to access cookies from javascript (not recommended)
        'httponly': True
    }
}

app = webapp2.WSGIApplication(ROUTES, config=config, debug=False)
