import httplib, urllib, base64, urllib2, json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html');

#def face_api_call(link):
#	print "\nFACE FEATURES API\n"
#	headers = {
#	'Content-Type': 'application/json',
#	'Ocp-Apim-Subscription-Key': '1255a5bd032544d39e72c04c7ba5a5bb',
#	}
#	params = urllib.urlencode({
#		'returnFaceId': 'true',
#		'returnFaceLandmarks': 'false',
#		'returnFaceAttributes': 'age,gender,smile',
#	})
#
#	try:
#		url = '{ "url" : "' + link + '"}'
#		conn = httplib.HTTPSConnection('api.projectoxford.ai')
#		conn.request("POST", "/face/v1.0/detect?%s" % params, url, headers)
#		response = conn.getresponse()
#		data = response.read()
#		print(data), "\n"
#		conn.close()
#	except Exception as e:
#		print("[Errno {0}] {1}".format(e.errno, e.strerror))
#
#
#def face_emotion_call(link):
#	print "\nFACE EMOTION API \n"
#	headers = {
#	'Content-Type': 'application/json',
#	'Ocp-Apim-Subscription-Key': '5d149c37b04a4d70b77490cfe027f868',
#	}
#	try:
#		url = '{ "url" : "' + link + '"}'
#		conn = httplib.HTTPSConnection('api.projectoxford.ai')
#		conn.request("POST", "/emotion/v1.0/recognize", url, headers)
#		response = conn.getresponse()
#		data = response.read()
#		print(data), "\n"
#		conn.close()
#	except Exception as e:
#			print("[Errno {0}] {1}".format(e.errno, e.strerror))
#

@app.route('/search', methods=['GET', 'POST'])
def search_ocr_call():
	print "\nQUERY SEARCH AND OCR API \n"
        query = request.form['searchbox']
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
	#print json_result

	for i in json_result['d']['results']:
		url = '{ "url" : "' + str(i['MediaUrl']) + '"}'
		try:
			conn = httplib.HTTPSConnection('api.projectoxford.ai')
			conn.request("POST", "/vision/v1/ocr?%s" % params, url, headers)
			response = conn.getresponse()
			data = response.read()
			json_result = json.loads(data)
			output = ''
			for r in json_result['regions']:
				for l in r['lines']:
					for w in l['words']:
						output += w['text']
						output += " "
			#print output, "\n"
                        print "Spellcheck: ", spellcheck(output)
			conn.close()
		except Exception as e:
			print("Error in ocr")
            
        
        
        return 'hello'
    
def spellcheck(input):
        headers = {
        # Request headers
                'Content-Type': 'application/x-www-form-urlencoded',
                'Ocp-Apim-Subscription-Key': '4526464118d644c4a791e8bf93d78591 ',
        }

        try:
                conn = httplib.HTTPSConnection('api.projectoxford.ai')
                text = '{"text" : "' + input + '"}'
                conn.request("POST", "/text/v1.0/spellcheck" , text , headers)
                response = conn.getresponse()
                data = response.read()
                #print(data)
                conn.close()
                return data
        except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
                
    

#def get_clarifai_tags(url):
#	print "\nCLARIFAI API\n"
#	method = "POST"
#	handler = urllib2.HTTPHandler()
#	opener = urllib2.build_opener(handler)
#	param = '{ "url" :"' + url + '"}'
#	data = urllib.urlencode(param)
#	request = urllib2.Request('https://api.clarifai.com/v1/tag', data)
#	request.add_header('Authorization', 'Bearer NbiYl9IAsjm75XqjS8gef0rZEeZTnS')
#	request.get_method = lambda: method
#	try:
#		connection = opener.open(request)
#	except urllib2.HTTPError,e:
#		connection = e
#
#	if connection.code == 200:
#		data = connection.read()
#		data = json.loads(data)
#		classList = data["results"][0]["result"]["tag"]["classes"]
#		print classList + "\n"
#
#def img_tag_category_call(link):
#	print "\nFEATURES - TAGS AND CATEGORIES \n"
#	headers = {
#	'Content-Type': 'application/json',
#	'Ocp-Apim-Subscription-Key': '55f752e2761b4c8492c4f12e9f9cd0e1',
#	}
#
#	params = urllib.urlencode({
#		'visualFeatures': 'All',
#	})
#	try:
#		url = '{ "url" : "' + link + '"}'
#		conn = httplib.HTTPSConnection('api.projectoxford.ai')
#		conn.request("POST", "/vision/v1/analyses?%s" % params, url, headers)
#		response = conn.getresponse()
#		data = response.read()
#		print(data), "\n"
#		conn.close()
#		get_clarifai_tags(link)
#	except Exception as e:
#		print("[Errno {0}] {1}".format(e.errno, e.strerror))
#
#link = "http://akonthego.com/blog/wp-content/uploads/2012/07/DSC_5129.jpg"
#face_api_call(link)
#face_emotion_call(link)
#search_ocr_call("life textonly quotes")
#img_tag_category_call(link)

if __name__ == "__main__":
    app.debug = True
    app.run()
