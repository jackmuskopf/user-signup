import webapp2
import random
import re

import cgi

def escape_html(s):
	return cgi.escape(s, quote = True)

header = """
		<!DOCTYPE html>
		<html>
		<head>
			<title>User-Signup</title>
		</head>
		<body>

		"""
footer = """
		</body>
		</html>

		"""
def color_text(text,color):
	return '<span style="color:'+color+';">'+text+"""</span><br/>"""


def add_errors(errors,form):
	splitform = form.split("</td></tr>")
	for error in errors:
		if error == invalid_username:
			splitform[0]+=color_text(invalid_username,'red')
		elif error == invalid_password:
			splitform[1]+=color_text(invalid_password,'red')
		elif error == invalid_confirm:
			splitform[2]+=color_text(invalid_confirm,'red')
		elif error == invalid_email:
			splitform[3]+= color_text(invalid_email,'red')
	error_form = "</tr></td>".join(splitform)
	return error_form



invalid_username = "Username can only contain numbers, letters, underscores, and hyphens. Must be 8 to 20 characters long."
invalid_password = "Password must be 8 to 20 characters long"
invalid_confirm = "Passwords do not match."
invalid_email = "Invalid email address"


class Index(webapp2.RequestHandler):
	 	def write_form(self, username = "",password="",confirm="",email="",errors=[]):
			form = """
			<h2>Sign Up</h2>
				<form method="post">
				<table>
				<tbody>
					<tr><td><span>Username: </span></td><td><input type="text" name="username"></td></tr>

					<tr><td><span>Password: </span></td><td><input type="password" name="password"></td></tr>

					<tr><td><span>Confirm Password: </span></td><td><input type="password" name="confirm"></td></tr>

					<tr><td><span>Email : </span></td><td><input type="text" name="email"></td></tr>

				</tbody>
				</table>
				<input type="submit">
				</form>

			      """
			if errors == []:
				if username == "":
					middle = form %{"username": username, "password": password, "confirm": confirm, "email": email} #%{"password": password} %{"confirm": confirm} %{"email": email}
					self.response.out.write(header+middle+footer)
				else:
					self.response.out.write(header+"<h2>Thank you for trusting me with your personal information, "+username+"</h2>"+footer)
			else:
				username = ""
				form = add_errors(errors,form)
				middle = form %{"username": username, "password": password, "confirm": confirm, "email": email}# %{"username": username} %{"password": password} %{"confirm": confirm} %{"email": email}
				self.response.out.write(header+middle+footer)

		def get(self):
			self.write_form()

		def post(self):
			errors = []
			username = self.request.get("username")
			password = self.request.get("password")
			confirm = self.request.get("confirm")
			email = self.request.get("email")
			if not re.match(r"^[a-zA-Z0-9_-]{8,20}$",username):
				errors.append(invalid_username)
			if not re.match(r"^.{8,20}$",password):
				errors.append(invalid_password)
			elif password != confirm:
				errors.append(invalid_confirm)
			if not re.match(r"^[\S]+@[\S]+.[\S]+$",email):
				errors.append(invalid_email)
			self.write_form(username = username, errors=errors)

app = webapp2.WSGIApplication([
	('/', Index),
], debug=True)
