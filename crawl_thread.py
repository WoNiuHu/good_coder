import threading
import time
import urlparse
import webpage_parse
import webpage_save
import url_table
import log


lock = threading.Lock()
#my_lock = thread.allocate_lock()


class CrawlThread(threading.Thread):

    def __init__(self, thread_id, directory, max_depth, pattern, interval=10, timeout=10):
        self._id = thread_id
        self._pattern = pattern
        self._interval = int(interval)
        self._timeout = timeout
        self._directory = directory
        self._max_depth = max_depth
        self.thread_stop = False
        threading.Thread.__init__(self)

    def run(self):
        log.info("thead %d is  running!" % self._id)
        while not self.thread_stop:
            lock.acquire()
            if url_table.url_queue.empty():
                log.info("url_table is empty, thread %d is exiting!" % self._id)
                self.stop()
                lock.release()
                continue
            info = url_table.url_queue.get()
            lock.release()
            url = info.get('url')
            depth = info.get('depth')
            log.info('thread-%d getting url %s' % (self._id, url))
            contents = webpage_parse.getWeb(url, self._pattern, self._timeout)
            if contents is None:
                log.info('thread-%d giving up url %s for return none')
                continue
            webpage_save.save_page(self._directory, url, contents)
            log.info('thread-%d saved page %s' % (self._id, url))
            url_table.url_table[url] = 1
            urls = webpage_parse.parseWeb(contents)
            depth += 1
            for i in urls:
                i = urlparse.urljoin(url, i)
                if depth > self._max_depth:
                    log.info("thread-%d depth:%d, over limit, pass" % (self._id, depth))
                    continue
                if(i in url_table.url_table.keys()):
                    log.info("thread-%d find duplicate url %s ignore!" % (self._id, url))
                    continue
                log.info("thread-%d put url %s, depth %d to queue" % (self._id, i, depth))
                element = {}
                element['url'] = i
                element['depth'] = depth
                lock.acquire()
                url_table.url_queue.put(element)
                lock.release()
            time.sleep(self._interval)

    def stop(self):
        self.thread_stop = True


def crawl(thread_num, directory, max_depth, pattern, interval, timeout):
    log.debug("now crawling with %d thread_num, %d depth, pattern %s!" % (thread_num, max_depth, pattern))
    for i in range(thread_num):
        MyThread = CrawlThread(i, directory, max_depth, pattern, interval, timeout)
        MyThread.start()
