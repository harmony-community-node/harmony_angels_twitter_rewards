from hashlib import sha1
from time import time
import base64
import json
import hmac
from secretes import Secretes
import requests

try:
    from urllib2 import (Request, urlopen)
except ImportError:
    from urllib.request import (Request, urlopen)

try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

#Initializations
follower_wonk_access_id_str = Secretes.follower_wonk_access_id_str
follower_wonk_secret_key_str = Secretes.follower_wonk_secret_key_str

#Class for access FollowerWonk API
class FollowerWonk(object):
    @staticmethod
    def social_authority(username):
        uri = 'https://api.followerwonk.com/social-authority'

        datime = int(time())
        
        keyBin = follower_wonk_secret_key_str.encode('UTF-8')
        messageStr = "%s\n%s" % (follower_wonk_access_id_str, datime)
        messageBin = messageStr.encode('UTF-8')

        s = hmac.new(keyBin, messageBin, sha1).digest()
        b64 = base64.b64encode(s)
        signature = quote_plus(b64)
        auth = "AccessID=%s;Timestamp=%s;Signature=%s" % (follower_wonk_access_id_str, datime, signature)       
        #print("%s?screen_name=%s;%s" % (uri, username, auth)) 
        result = requests.get("%s?screen_name=%s;%s" % (uri, username, auth), allow_redirects=False)
        #print(result.content)

        responseStr = result.content.decode("utf-8")
        response_Json = {}
        try:
            response_Json = json.loads(responseStr)
            #print(f'Followerwonk response {response_Json}')
        except  Exception as ex:
            print(ex)
            return ''

        if '_embedded' not in response_Json:
            return ''

        return response_Json['_embedded']