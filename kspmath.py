#!/usr/bin/env python
#coding=utf-8

from flask import Flask,render_template,request
from flask_apscheduler import APScheduler
from showimage import showimg
import math

app = Flask(__name__)

app.register_blueprint(showimg , url_prefix='/showimg')

@app.route('/' , methods=['GET','POST'])
def kspform():
	if request.method == 'GET':
		return render_template('kspform.html')

	if request.method == 'POST':
		print request.form
		fullheavy = float(request.form['fullheavy'])
		emptyheavy = request.form['emptyheavy']
		if emptyheavy != '':
			emptyheavy = float(emptyheavy)
		thrust = float(request.form['thrust'])

		if request.form['num'] == '':
			num = 1
		else:
			num = float(request.form['num'])

		isp = request.form['isp']
		if isp != '':
			isp = float(isp)
		planetg = float(request.form['planetg'])
		
		twr = thrust * num / fullheavy / planetg
		twr16 = 1.6 / twr
		twr18 = 1.8 / twr
		twr20 = 2 / twr

		delta_v = 0		
		if emptyheavy != '':
			delta_v = isp * planetg * math.log(fullheavy / emptyheavy)

		msg = u'推重比：%.2f ，twr1.6: %.2f , twr1.8: %.2f , twr2.0: %.2f , DV：%.2f'%(twr,twr16,twr18,twr20,delta_v)
		#twrmsg = u'twr 1.6: %.2f'
		return render_template('kspform.html' , fullheavy=fullheavy , emptyheavy=emptyheavy , thrust=thrust , num=num , isp=isp ,msg=msg)


class Config():
	JOBS = [
    {
        'id': 'job1',
        'func': '__main__:hello',
        'args': None,
        'trigger': 'interval',
        'seconds': 5
    }
	]
	SCHEDULER_API_ENABLED = True

def hello():
	print 'hello world'

app.config.from_object(Config)
scheduler=APScheduler()
scheduler.init_app(app)


if __name__ == '__main__':
	scheduler.start()
	app.run(port=5000 , debug=True)