
#coding=gbk

from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
	if 'username' in session:
		return 'Logged in as %s' % session['username']

	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['checkcode'] == session['checkcode']:
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			#mess = u'验证码错误'
			return 'checkfalse'

	if request.method == 'GET':
		return render_template('sessionmode.html' , user='')
	
@app.route('/check' , methods=['GET','POST'])
def checkcode():
	if request.method == 'POST':
		print request.form
		username = request.form['username']
		checkcode = '123456'
		print checkcode
		session['checkcode'] = checkcode
		return 'checkcode was send'

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0' , port = 5000)