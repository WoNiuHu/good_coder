import sys
import log
import url_table


def loadSeedFile(file):
    try:
        for line in open(file):
            line = line.rstrip()
            element = {}
            element['url'] = line
            element['depth'] = 0
            url_table.url_queue.put(element)
    except Exception, e:
        log.error("can't open file: " + file + ", ReasonCode: " + str(e))
        sys.exit()
