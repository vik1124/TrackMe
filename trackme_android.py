import time
import accesssqlite as db
import android
import urllib2
import urllib

url = 'http://vik1124.pythonanywhere.com/Access'
qa = { 'loginid':'', 'pwd':'' ,'lati':'','longi':''}

droid = android.Android()


def SendData(data):
	try:
		request = urllib2.Request(url,data)
		response = urllib2.urlopen(request)
		res = response.read().rstrip()
		print res
		if res == 'NAT':
			db.DeleteCredentials()
			print "Invalid User Info"
		lc=0
		while res=='NCK' and lc<3:
			print "in loop"
			response = urllib2.urlopen(request)
			res = response.read().rstrip()
			if res == 'NAT':
				db.DeleteCredentials()
			lc+=1
		if res == 'ACK':
			print "Sent!"
		else:
			print "Error in Sending Data!"
	except:
		print "error"
	
def send_coords():
	global qa
	cred = db.GetCredentials()
	droid.startLocating()
	time.sleep(25)
	loc= droid.readLocation().result
	print loc
	if loc=={}:
		loc = droid.getLastKnownLocation().result
		print "lastloc"
	try:
	    n = loc['gps']
	except KeyError:
		n = loc['network']
	qa['loginid'] = cred[0]
	qa['pwd'] = cred[1]
	qa['lati'] = n['latitude'] 
	qa['longi'] = n['longitude']
	data = urllib.urlencode(qa)
	SendData(data)
	droid.stopLocating()
	
if __name__ == "__main__":
	db.LoginUser()
	i=0
	send_coords()
	a=time.time()
	while 1:
		time.sleep(600)
		print time.time() - a
		if (time.time() - a) >1799:
			send_coords()
			i=i+1
			a=time.time()
	print "Done"