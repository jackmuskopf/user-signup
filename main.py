import webapp2
import random

import cgi

def escape_html(s):
	return cgi.escape(s, quote = True)

header = """
		<!DOCTYPE html>
		<html>
		<head>
			<title>caesar</title>
		</head>
		<body>

		"""
footer = """
		</body>
		</html>

		"""
def color_text(text,color):
	return '<span style="color:'+color+';">'+text+"""</span><br/>"""

def bad_un(name):
	for c in name:
		if (not c.isalpha() and not c.isdigit()) and c != '_':
			return True
	return False

def add_errors(errors,form):
	print errors
	splitform = form.split("<br><br>")
	for error in errors:
		print error
		if error == invalid_username:
			splitform[0]+=color_text(invalid_username,'red')
		elif error == invalid_password:
			splitform[1]+=color_text(invalid_password,'red')
		elif error == invalid_confirm:
			splitform[2]+=color_text(invalid_confirm,'red')
		error_form = "<br><br>".join(splitform)
		print error_form
	return error_form


	#   form = """
    # <!DOCTYPE html>
    #   <html>
    #   <head>
    #   <title>Unit 2 Rot 13</title>
    #   </head>
    #   <body>
    #   <h2>Enter some text to ROT13:</h2>
    #   <form method="post">
    #   <textarea name="text" style="height: 100px; width: 400px; ">
    #   %(content)s
    #   </textarea>
    #   <br>
    #
    #   </form>
    #   </body>
    # #   </html>
    #   """




invalid_username = "Username can only contain numbers, letters, and underscores. Must be at least 8 characters long."
invalid_password = "Password must be at least 8 characters long"
invalid_confirm = "Passwords do not match."
errorMSG = "Key has to be a number"

class Index(webapp2.RequestHandler):
	 	def write_form(self, username = "",password="",confirm="",email="",errors=[]):
			form = """
			<h2>Sign Up</h2>
				<form method="post">
					<span>Username: </span><input type="text" name="username">%(username)s
					<br><br>
					<span>Password: </span><input type="password" name="password">%(password)s
					<br><br>
					<span>Confirm Password: </span><input type="password" name="confirm" >%(confirm)s
					<br><br>
					<span>Email(optional): </span><input type="text" name="email">%(email)s
					<br><br>
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
			if len(username) < 8 or bad_un(username):
				errors.append(invalid_username)
			if len(password) < 8:
				print 'yep'
				errors.append(invalid_password)
			elif password != confirm:
				errors.append(invalid_confirm)
			self.write_form(username = username, errors=errors)

# class Index(webapp2.RequestHandler):
#
# 	# def get(self):
# 	def get(self):
# 		form = """
# 			<h1>Caesar Text</h1>
# 			<form action="/action_page.php">
# 			  Text: <input type="text" name="intext"><br>
# 			  Key: <input type="text" name="num"><br>
# 			  <input type="submit" value="Submit">
# 			</form>
# 		"""
# 		self.response.write(header+form+footer)
#
# 	def post(self):
# 		form = """
# 			<h1>{0}</h1>
# 		""".format(caesar(self.request.get("intext"),self.request.get("num")))
# 		self.response.write(header+form+footer)

# class GenNum(webapp2.RequestHandler):
#
#
# 	def get(self):
# 		badmessage = "<strong>Only people who click the button are lucky...</strong>"
# 		self.response.write(header+badmessage+footer)
#
# 	def post(self):
# 		lucky = str(random.randint(0,100))
# 		successmesssage=header+"<strong>"+lucky+"</strong> is your lucky number!"+footer
# 		self.response.write(successmesssage)
#


app = webapp2.WSGIApplication([
	('/', Index),
], debug=True)
