import httplib, urllib, base64, urllib2, json
#from flask import Flask, render_template, request

#app = Flask(__name__)

#@app.route('/')
#def hello():
#    return render_template('index.html');

CLARIFAI_ID = '9GCHk6DcJOqdGx_KT3WbLb2JVUHYUhUkfF7HfC2J'
CLARIAI_SECRET = 'g6MxcRw_Ou0cb2c_PkQleV1UirufHZgL2o69o7Fy'

def getClarifaiToken():
	method = "POST"
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	values = {'grant_type':'client_credentials','client_id':CLARIFAI_ID, 'client_secret':CLARIAI_SECRET}
	data = urllib.urlencode(values)
	request = urllib2.Request("https://api.clarifai.com/v1/token/", data)
	request.get_method = lambda: method
	try:
		connection = opener.open(request)
	except urllib2.HTTPError,e:
		connection = e
	if connection.code == 200:
		data = connection.read()
	else:
		print "Clarifai connection error"
	data = json.loads(data)	
	return data['access_token']

def face_api_call(link):
	print "\nFACE FEATURES API\n"
	headers = {
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': '1255a5bd032544d39e72c04c7ba5a5bb',
	}
	params = urllib.urlencode({
		'returnFaceId': 'true',
		'returnFaceLandmarks': 'false',
		'returnFaceAttributes': 'age,gender,smile',
	})

	try:
		url = '{ "url" : "' + link + '"}'
		conn = httplib.HTTPSConnection('api.projectoxford.ai')
		conn.request("POST", "/face/v1.0/detect?%s" % params, url, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		return data
	except Exception as e:
		pass
		#print("[Errno {0}] {1}".format(e.errno, e.strerror))


def face_emotion_call(link):
	print "\nFACE EMOTION API \n"
	headers = {
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': '5d149c37b04a4d70b77490cfe027f868',
	}
	try:
		url = '{ "url" : "' + link + '"}'
		conn = httplib.HTTPSConnection('api.projectoxford.ai')
		conn.request("POST", "/emotion/v1.0/recognize", url, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		return data
	except Exception as e:
		pass
		#print("[Errno {0}] {1}".format(e.errno, e.strerror))


def search_ocr_call(query):
	print "\nQUERY SEARCH AND OCR API \n"
	headers = {
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': '55f752e2761b4c8492c4f12e9f9cd0e1',
	}
	params = urllib.urlencode({
		'language': 'unk',
		'detectOrientation ': 'true',
	})

	search_type = "Image"
	key= 'FNCeR+bi9PhI9JjDXKmpZ3rUkGWWJ3Zz7M72PQDCniQ'
	query = urllib.quote(query)

	credentials = (':%s' % key).encode('base64')[:-1]
	auth = 'Basic %s' % credentials
	url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=10&$format=json'
	request = urllib2.Request(url)
	request.add_header('Authorization', auth)
	request_opener = urllib2.build_opener()
	response = request_opener.open(request) 
	response_data = response.read()
	json_result = json.loads(response_data)
	output_list = ""
	for i in json_result['d']['results']:
		url = '{ "url" : "' + str(i['MediaUrl']) + '"}'
		try:
			conn = httplib.HTTPSConnection('api.projectoxford.ai')
			conn.request("POST", "/vision/v1/ocr?%s" % params, url, headers)
			response = conn.getresponse()
			data = response.read()
			json_result = json.loads(data)
			output = ''
			#print json_result
			for r in json_result['regions']:
				for l in r['lines']:
					for w in l['words']:
						output += w['text']
						output += " "
			output_list = output_list + "|" + output
			conn.close()
		except Exception as e:
			pass
			#print("Error in OCR", e)
	output_list = output_list.encode("ascii", "ignore")
	quotes = spellcheck(str(output_list))
	caption_list = []
	print quotes
	caption_list = quotes[1:].split('|')
	return caption_list

def spellcheck(quote):
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Ocp-Apim-Subscription-Key': 'e56e9260807b4bca9ef3758ee6a94998',
	}

	try:
		conn = httplib.HTTPSConnection('api.projectoxford.ai')
		text = 'Text=' + quote
		conn.request("POST", "/text/v1.0/spellcheck" , text , headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		json_result = json.loads(data)
		json_result['spellingErrors'].sort(key=lambda i:i['offset'], reverse=True)
		
		for correction in json_result['spellingErrors']:
			current = correction['token']
			new = correction['suggestions'][0]['token']
			quote = quote[:correction['offset']] + new + quote[correction['offset'] + len(current):]
		return quote
	except Exception as e:
		pass
		#print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_clarifai_tags(url):
	method = "POST"
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	param = {'url':url}
	data = urllib.urlencode(param)
	request = urllib2.Request('https://api.clarifai.com/v1/tag', data)
	request.add_header('Authorization', 'Bearer ' + getClarifaiToken())
	request.get_method = lambda: method
	try:
		connection = opener.open(request)
	except urllib2.HTTPError,e:
		connection = e
	if connection.code == 200:
		data = connection.read()
	else:
		print "Clarifai connection error"
	data = json.loads(data)
	classList = data["results"][0]["result"]["tag"]["classes"]
	print classList[:5]
	return classList


def img_tag_category_call(link):
	print "\nFEATURES - TAGS AND CATEGORIES \n"
	headers = {
	'Content-Type': 'application/json',
	'Ocp-Apim-Subscription-Key': '55f752e2761b4c8492c4f12e9f9cd0e1',
	}

	params = urllib.urlencode({
		'visualFeatures': 'All',
	})
	try:
		url = '{ "url" : "' + link + '"}'
		conn = httplib.HTTPSConnection('api.projectoxford.ai')
		conn.request("POST", "/vision/v1/analyses?%s" % params, url, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		return data
	except Exception as e:
		pass
		#print("[Errno {0}] {1}".format(e.errno, e.strerror))

def extract_tags(face_attr, face_emo, img_tag, img_tags_clarifai):
	tags = img_tags_clarifai[0] + ' textonly ' + 'quotes'
	print "TAGS: ", tags
	return tags

def get_img_caption(link):
	face_attr = face_api_call(link)
	face_emo = face_emotion_call(link)
	img_tag = img_tag_category_call(link)
	img_tags_clarifai = get_clarifai_tags(link)
	print face_attr, "\n"
	print face_emo, "\n"
	print img_tag, "\n"
	print img_tags_clarifai, "\n"
	tags = extract_tags(face_attr, face_emo, img_tag, img_tags_clarifai)
	quote_list = search_ocr_call(tags)
	print "\nCAPTIONS/QUOTES\n"
	for quote in quote_list:
		print quote, "\n"
	return quote_list

def get_giphy(tags):
	url = "http://api.giphy.com/v1/gifs/search?q=" + tags + "&api_key=dc6zaTOxFJmzC"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	url_list = []
	for i in range(20):
		url_list.append(data['data'][i]['images']['fixed_height']['url'])
	print url_list
	return url_list

link = "http://www.hiltonhawaiianvillage.com/assets/img/discover/oahu-island-activities/HHV_Oahu-island-activities_Content_Beaches_455x248_x2.jpg"
tags = "kid beach"
get_img_caption(link)
get_giphy(tags)

#if __name__ == "__main__":
#    app.debug = True
#    app.run()
