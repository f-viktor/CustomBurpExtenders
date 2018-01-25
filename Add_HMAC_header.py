###################################################
### Custom extender to add headers to requests  ###
### Add it to a session handling rule to use    ###
### Tested in BurpSuitePro 1.7.30  jhyton 2.7.0 ### 
###################################################

from burp import IBurpExtender
from burp import ISessionHandlingAction
from burp import IParameter
import hmac
import base64
import hashlib
import time

class BurpExtender(IBurpExtender, ISessionHandlingAction):

#
# implement IBurpExtender
#

	def registerExtenderCallbacks(self, callbacks):

		# keep a reference to our callbacks object
		self._callbacks = callbacks

		# keep a reference to the callback helpers
		self._helpers = callbacks.getHelpers()

		callbacks.setExtensionName("Insert Custom HTTP Header")

		# Register Session Handling Action
		callbacks.registerSessionHandlingAction(self)

		return

	def getActionName(self):
		return "Insert Custom HTTP Header"

	def performAction(self, currentRequest, macroItems): #void performAction(IHttpRequestResponse currentRequest, IHttpRequestResponse[] macroItems)
		requestInfo = self._helpers.analyzeRequest(currentRequest)
		headers = requestInfo.getHeaders()
		msgBody = currentRequest.getRequest()[requestInfo.getBodyOffset():]
		msgUrl = requestInfo.getUrl()

		#cheap solution will not work if your uri is in proxy format, or different port
		msgUri= msgUrl.toString().split(":443",1)[1]
		
		# Add your Custom Header values Here
		ClientID= '<PUT_YOUR_USER_HERE>'
		key= '<PUT_YOUR_KEY/PASSWORD_HERE>'
		timestamp= str(int(time.time()*1000))
		
		#Change this depending on your signiture format
		signiture= ClientID+key+'GETapplication/json'+msgUri+timestamp
		signiture= signiture.replace('?', '')	

		#Create HMAC
		signiture= base64.b64encode(hmac.new(key,signiture,hashlib.sha256).digest())

		#Add the custom headers
		headers.add('clientID: %s' % ClientID)
		headers.add('timestamp: %s' % timestamp)
		headers.add('Content-Type: application/json')
		headers.add('signature: %s' % signiture)		

		# Build new Http Message with the new custom Header
		message = self._helpers.buildHttpMessage(headers, msgBody)

		# Print Header into UI
		print self._helpers.bytesToString(message)

		# Update Request with New Header
		currentRequest.setRequest(message)
		return 
