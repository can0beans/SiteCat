from xml.dom import minidom
import sys
from pywebshot import *
import gtk
import gtk.gdk as gdk

def writeBeginning(filehandle):
	text = """<html>
<head>
	<title>SiteCat Seez Ur Sites</title>
	<style type="text/css">
	body {
    margin:0px;
    }
    #hits {
        position: absolute;
        top:0px;
        left:0px;
        width:10%;
        height:200%;
    }
    #dframe {
        position:absolute;
        top:0px;
        left:20%;
        width:90%;
        height:300%;
      }
    </style>
    <script type="text/javascript">
    </script>
</head>
<body>
    <div id="hits" class="resultsList">
	<img src="sitecat.jpg">
	"""
	filehandle.write(text)

def writeUrl(port, interestingPorts):
	if (port in interestingPorts):
			port=str(port)
			if (port == "443"):
				url = "https://" + ipAddress
				return url
			elif (port == "80"):
				url = "http://" + ipAddress
				return url
			else: 
				url = "http://" + ipAddress + ":" + port
				return url

def writeEnd(filehandle):
	end = """</div>
    <iframe id="dframe" name="dframe">
    </iframe>
</body>
</html>"""
	filehandle.write(end)
	
	

def writeIframe(hostUrl, filehandle):
		filehandle.write('<a href="' + hostUrl + '/" target="dframe">' + hostUrl + '</a>\n') 

def __windowExit(widget, data=None):
	gtk.main_quit()

def grabScreen(hostUrlList):
	screen = "640x480"
	delay = 1
	thumbnail = "350x200"
	window = PyWebShot(hostUrlList, screen,thumbnail,delay, outfile)
	window.parent.connect("destroy", __windowExit)
	gtk.main()
	




outputFile = open('iframe.html', 'w')
xmldoc = minidom.parse('output.xml')
interestingPorts = [80,443,8080]


writeBeginning(outputFile)

for dhost in  xmldoc.getElementsByTagName('host'):
	ipAddress = str(dhost.getElementsByTagName('address')[0].getAttributeNode('addr').value)
	for dport in dhost.getElementsByTagName('port'):
		proto = dport.getAttributeNode('protocol').value
		port =  int(dport.getAttributeNode('portid').value)
		state = dport.getElementsByTagName('state')[0].getAttributeNode('state').value
		reason = dport.getElementsByTagName('state')[0].getAttributeNode('reason').value
		
		hostUrl = writeUrl(port, interestingPorts)
		if (hostUrl):
			print hostUrl
			writeIframe(hostUrl, outputFile)
			outfile = ipAddress + ".png"
			print outfile
			hostUrlList = [hostUrl]
			print hostUrlList
			grabScreen(hostUrlList)			
			


			
writeEnd(outputFile)				
outputFile.close()		
