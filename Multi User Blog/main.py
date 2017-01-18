#!/usr/bin/env python
import webapp2
from handlers.index import IndexHandler
from handlers.auth import Register, LoginHandler, LogoutHandler
from handlers.blog import AddBlog, EditBlog, Permalink, BlogList, DeleteBlog
from handlers.comment import AddComment, DeleteComment, CommentError, UpdateComment
from handlers.likes import LikeBlog, LikeError


app = webapp2.WSGIApplication([
    ('/', BlogList),
    ('/allposts', BlogList),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/register', Register),
    ('/blog/add', AddBlog),
    ('/blog/edit/([0-9]+)', EditBlog),
    ('/blog/like/([0-9]+)', LikeBlog),
    ('/blog/delete/([0-9]+)', DeleteBlog),
    ('/blog/([a-z0-9\-]+)', Permalink),
    ('/blog/([0-9]+)/add/comment', AddComment),
    ('/delete/comment/([0-9]+)', DeleteComment),
    ('/edit/comment/([0-9]+)', UpdateComment),
    ('/comment/error', CommentError),
    ('/like/error', LikeError),
], debug=True)
