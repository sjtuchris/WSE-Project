import urllib2
import re
import sys

# Download data from Webrobots
folder = sys.argv[1]
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request("http://webrobots.io/kickstarter-datasets", None, headers)
html = urllib2.urlopen(req).read()
pattern = 'https://s3.amazonaws.com/weruns/forfun/Kickstarter/[a-zA-Z0-9.\-_/]+'
links = re.findall(pattern, html)

# download 
for link in links:
    try:
        print link
        res = urllib2.urlopen(link)
        content = res.read()
        # write to file
        file_name = link[link.rindex('/'):]
        file = open(folder + '/data'+file_name, 'w')
        file.write(content)
        file.close()

    except Exception, e:
        print "error while retrieving data: ", e