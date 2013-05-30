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
import cgi
import re

form=   """
        <h2>Enter some text to ROT13:</h2>
        <form method="post">
            <textarea name='text' cols='55' rows='10'>%(text)s</textarea>         
            <br>
            <input type="submit">
        </form>
        """

signup= """
        <h2>Signup</h2>
        <form method="post">
          <table>
            <tr>
              <td class="label">
                Username
              </td>
              <td>
                <input type="text" name="username" value="%(username)s">
              </td>
              <td class="error">
                <div style="color:red">%(user_error)s</div>
              </td>
            </tr>

            <tr>
              <td class="label">
                Password
              </td>
              <td>
                <input type="password" name="password" value="">
              </td>
              <td class="error">
                <div style="color:red">%(password_error)s</div>
              </td>
            </tr>

            <tr>
              <td class="label">
                Verify Password
              </td>
              <td>
                <input type="password" name="verify" value="">
              </td>
              <td class="error">
                <div style="color:red">%(verify_error)s</div>
              </td>
            </tr>

            <tr>
              <td class="label">
                Email (optional)
              </td>
              <td>
                <input type="text" name="email" value="%(email)s">
              </td>
              <td class="error">
                <div style="color:red">%(email_error)s</div>
              </td>
            </tr>
          </table>

          <input type="submit">
        </form>
        """

message="""
        <h2>Welcome, %(username)s!</h2>
        """

class MainHandler(webapp2.RequestHandler):
    def write_form(self, text=""):
        self.response.out.write(form % {"text": text})                  
        
    def get(self):
        self.write_form()

    def post(self):
        user_text = self.request.get('text')
        text = cgi.escape(rot13(user_text), quote=True)
        
        self.write_form(text)

class SignupHandler(webapp2.RequestHandler):
    def write_form(self, user_error="", password_error="", verify_error="",
                   email_error="", username="", email=""):
        self.response.out.write(signup % {"user_error":user_error,
            "password_error":password_error, "verify_error":verify_error,
            "email_error":email_error, "username":username, "email":email})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        user_error = ""
        password_error = ""
        email_error = ""
        verify_error = ""

        if not valid_username(username):
            user_error = "That's not a valid username."
        if not valid_password(password):
            password_error = "That wasn't a valid password."
        if not valid_email(email):
            email_error = "That's not a valid email."
        if verify != password:
            verify_error = "Your passwords didn't match."

        if user_error or password_error or email_error or verify_error:    
            self.write_form(user_error, password_error, verify_error,
                email_error, username, email)
        else:
            self.redirect("/welcome?username=%s" % username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write(message % {'username':username})

def rot13(text):
    cypher = {'a':'n', 'b':'o', 'c':'p', 'd':'q', 'e':'r', 'f':'s', 
              'g':'t', 'h':'u', 'i':'v', 'j':'w', 'k':'x', 'l':'y', 
              'm':'z', 'n':'a', 'o':'b', 'p':'c', 'q':'d', 'r':'e', 
              's':'f', 't':'g', 'u':'h', 'v':'i', 'w':'j', 'x':'k', 
              'y':'l', 'z':'m', 'A':'N', 'B':'O', 'C':'P', 'D':'Q', 
              'E':'R', 'F':'S', 'G':'T', 'H':'U', 'I':'V', 'J':'W', 
              'K':'X', 'L':'Y', 'M':'Z', 'N':'A', 'O':'B', 'P':'C',
              'Q':'D', 'R':'E', 'S':'F', 'T':'G', 'U':'H', 'V':'I', 
              'W':'J', 'X':'K', 'Y':'L', 'Z':'M'}
              
    encrypted = []
    encrypted_text = ''   
    for letter in text:
        encrypted.append(letter)       
    for i in range(len(encrypted)):
        if encrypted[i] in cypher:
            encrypted[i] = cypher[encrypted[i]]
            encrypted_text += encrypted[i]
        else:
            encrypted_text += encrypted[i]
    return encrypted_text

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)
       
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/signup', SignupHandler),
                               ('/welcome', WelcomeHandler)],
                              debug=True)
