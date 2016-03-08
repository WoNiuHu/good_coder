#import sys
import os
import urllib2
import log


def save_page(directory, url, contents):
    if not os.path.exists(directory):
        os.makedir(directory)
    try:
        f = file(directory + "/" + urllib2.quote(url, ' '), 'w')
        f.write(contents)
        f.close()
    except Exception, e:
        log.error('Error in saving url ' + url + ', Reason: ' + str(e))
