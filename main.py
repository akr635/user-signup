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
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        User Signup
    </h1>
"""

page_footer = """
</body>
</html>
"""

form = """
    <form method="post">
        <label>Username
            <input name="username" type="text" value="%(username)s">
            <span class="error">%(username_error)s</span>
        </label>
                <br>
        <label>Password
            <input name="password" type="password" value="">
            <span class="error">%(password_error)s</span>
        </label>
                <br>
        <label>Verify Password
            <input name="verify" type="password" value=""/>
            <span class="error">%(verify_error)s</span>
        </label>
                <br>
        <label>Email (optional)
            <input name="email" type="email" value="%(email)s">
            <span class="error">%(email_error)s</span>
        </label>
                <br>
        <input type="submit">
    </form>
    """

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):

    def write_form(self, username="", username_error="", password_error="",
    verify_error="", email="", email_error=""):
        content = page_header + form + page_footer
        self.response.write(content % {"username": username,
                                        "username_error": username_error,
                                        "password_error": password_error,
                                        "verify_error": verify_error,
                                        "email": email,
                                        "email_error": email_error})

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")


        username_error = ""
        if not valid_username(username):
            username_error += "Please enter a valid username."

        password_error = ""
        if not valid_password(password):
            password_error += "Please enter a valid password."

        verify_error = ""
        if password != verify:
            verify_error += "Your passwords don't match."

        email_error = ""
        if not valid_email(email):
            email_error += "Your email address is not valid."

        if not (valid_username and valid_password and password == verify and
        valid_email):
            self.write_form(username, username_error, password_error,
            verify_error, email, email_error)
        else:
            self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")

        welcome_message = "Welcome, %(username)s." % {"username": username}
        welcome_content = page_header + "<p>" + welcome_message + "</p>" + page_footer
        self.response.write(welcome_content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
