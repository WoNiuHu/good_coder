import urllib2
import socket
import re
import log
import HTMLParser


class MyParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == 'a':
            if len(attrs) == 0:
                pass
            else:
                # judge label a
                pattern = re.compile(r'javascript')
                for name, value in attrs:
                    if name == 'href':
                        if pattern.match(value):
                            p = re.match(r'javascript:location.href=[\'\"]?([\w\.\d\_\-]+)[\'\"]?', value)
                            if p:
                                self.links.append(p.expand(r'\1'))
                        else:
                            self.links.append(value)


def getWeb(url, pattern, timeout):
    try:
        f = urllib2.urlopen(url, timeout=timeout)
    except urllib2.URLError, e:
        if hasattr(e, 'code'):
            log.error('Error in open url: ' + url + ', ErrorCode:' + str(e.code))
            return None
        elif hasattr(e, 'reason'):
            log.error('Error in open url: ' + url + ', Reason:' + str(e.reason))
            return None
    except socket.timeout, e:
        log.error("timeout in get url: " + url)
        return None
    except Exception, e:
        log.error("unkown exception:" + str(e))
        return None
    contents = f.read()
    return contents


def parseWeb(contents):
    my = MyParser()
    my.feed(contents)
    my.close()
    return my.links
