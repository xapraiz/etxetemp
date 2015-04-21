#!/usr/bin/env python

import webapp2
import httplib2
import urllib
import json
import base64
import random
import time
import hmac
import binascii
import hashlib
import logging
import jinja2
import os
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        #self.session['twitter_user'] = False
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext
        }

        template = JINJA_ENVIRONMENT.get_template('jinja_template.html')
        self.response.write(template.render(template_values))





#############
## DROPBOX ##
#############

class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'my-super-secret-key'}




dropbox_app_key='kq1dnywotn5al03'
gae_callback_url='https://etxetemp.appspot.com/oauth_callbackDropbox'
dropbox_app_secret=''

class LoginAndAuthorizeDropbox(webapp2.RequestHandler):
    def get(self):

        url='https://www.dropbox.com/1/oauth2/authorize'
        parametroak= {'response_type':'code',
                      'client_id':dropbox_app_key,
                      'redirect_uri':gae_callback_url
        }
        parametroak=urllib.urlencode(parametroak)
        self.redirect(url + '?' + parametroak)



class OAuthCallbackDropbox(BaseHandler):
    def get(self):
        request_url= self.request.url
        code=request_url.split('code=')[1]

        http=httplib2.Http()
        metodoa='POST'
        url='https://api.dropbox.com/1/oatuh2/token'
        parametroak={'code':code,
                     'grant_type': 'authorization.code',
                     'client_id': dropbox_app_key,
                     'client_secret':dropbox_app_secret,
                     'redirect_uri':gae_callback_url}

        parametroak=urllib.urlencode(parametroak)
        erantzuna, edukia=http.request(url, metodoa,body=parametroak, headers={})

        #self.response.write(edukia)

        json_edukia= json.load(edukia)
        self.session['access_token']=json_edukia['access_token']
        self.redirect('/welcomePage')




class WelcomePageDropbox(BaseHandler):
    def get(self):
        access_token=self.session['access_token']

        http=httplib2.Http()
        method='PUT'
        path='/karpeta/fitxategia.txt'
        url='https://api-content.dropbox.com/1/files_put/auto' + path
        parametroak={'overwrite':'false'}
        parametroak=urllib.urlencode(parametroak)
        goiburuak={}
        goiburuak['Authorization']='Bearer ' + access_token
        edukia='Hau fitxategiaren eduki da,,, probaa'
        resp, content = http.request(url + '?' + parametroak, method, body=edukia, headers=goiburuak)

        self.response.write('Egiaztatu zure Dropbox kontuan fitxategia sortu dela')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/LoginAndAuthorizeDropbox', LoginAndAuthorizeDropbox),
    ('/oauth_callbackDropbox', OAuthCallbackDropbox),
    ('/welcomePageDropbox', WelcomePageDropbox)
], debug=True)
