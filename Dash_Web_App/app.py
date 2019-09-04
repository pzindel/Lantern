#import libraries
import dash
import dash_auth
import sqlite3

#open connection with user database
connection = sqlite3.connect("database/usernames.db")
cur = connection.cursor()

#retrieve usernames and passwords
cur.execute('SELECT username, password FROM user')
VALID_USERNAME_PASSWORD = cur.fetchall()

#import a css stylesheet (provided through Dash documentation)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#initialize app with css and check for user login
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD)
app.config.suppress_callback_exceptions = True