import httplib
import urlparse
import urllib

from lab1.pymd5 import md5, padding


# change these two line if use command line
# url = sys.argv[1]
url = 'http://www.cs.bu.edu/~goldbe/teaching/HW55814/lab1/' \
      'api?' \
      'token=11ed1b5786c5fc4d4fa4294f4d281df1&' \
      'user=sgoldberg&' \
      'command1=ListFiles&command2=NoOp'

parsedUrl = urlparse.urlparse(url)
query = parsedUrl.query
# split query into two parts, the first is md5 of original message, second is the original message
token, message = query.split('&', 1)
# get the token value
token = token.split('=')[1]
op3 = '&command3=DeleteAllFiles'
#bits of message after padding, secret is 8 bits so the total origin length is len(message)+8
bits = (len(message) + 8 + len(padding((len(message)+8) * 8))) * 8
h = md5(state=token.decode('hex'), count=bits)
h.update(op3)
newToken = h.hexdigest()
newMessage = message + urllib.quote(padding((len(message)+8) * 8)) + op3
newQuery = 'token=%s&%s' % (newToken, newMessage)

print 'message:\t'+message
print 'token:\t'+token
print 'newMessage:\t'+newMessage
print 'newToken:\t'+newToken
print 'newQuery:\t'+newQuery

conn = httplib.HTTPConnection(parsedUrl.hostname)
conn.request("GET", parsedUrl.path + '?' + newQuery)
print conn.getresponse().read()
