from flask import Flask, render_template
import urllib
import urllib2
import json

import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
}

params = urllib.urlencode({
    # Request parameters
    # Specify your subscription key
    'subscription-key': 'd419aa0bcc0a415fb1760bae4f2670a7',
    'language': 'unk',
    'detectOrientation ': 'true',
})

app = Flask(__name__)

@app.route("/")
def hello():
    query = "life quotes"
    search_type = "Image"
    key= 'FNCeR+bi9PhI9JjDXKmpZ3rUkGWWJ3Zz7M72PQDCniQ'
    query = urllib.quote(query)
    
    # create credential for authentication
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"
    credentials = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=10&$format=json'
    request = urllib2.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request) 
    response_data = response.read()
    json_result = json.loads(response_data)
    
    for i in json_result['d']['results']:
        url = "{" + str(i['MediaUrl'].encode('ascii', 'ignore')) + "}"
        print url
        
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
            print output
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
    return string(output)

if __name__ == "__main__":
    app.run()
