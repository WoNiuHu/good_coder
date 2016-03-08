import threading
import time
import urlparse
import log
import webpage_parse
import webpage_save
import url_table


lock4queue = threading.Lock()
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
        self.status = 0
        threading.Thread.__init__(self)

    def run(self):
        log.info("thead %d is  running!" % self._id)
        while not self.thread_stop:
            lock4queue.acquire()
            if url_table.url_queue.empty():
                log.info("url_table is empty, thread %d is holding!" % self._id)
                self.status = 0
                lock4queue.release()
                time.sleep(1)
                continue
            info = url_table.url_queue.get()
            self.status = 1
            lock4queue.release()
            url = info.get('url')
            depth = info.get('depth')
            log.info('thread-%d getting url %s' % (self._id, url))
            contents = webpage_parse.getWeb(url, self._pattern, self._timeout)
            if contents is None:
                log.info('thread-%d giving up url %s for return none')
                self.status = 0
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
                    self.status = 0
                    continue
                if(i in url_table.url_table.keys()):
                    log.info("thread-%d find duplicate url %s ignore!" % (self._id, url))
                    self.status = 0
                    continue
                log.info("thread-%d put url %s, depth %d to queue" % (self._id, i, depth))
                element = {}
                element['url'] = i
                element['depth'] = depth
                lock4queue.acquire()
                url_table.url_queue.put(element)
                self.status = 0
                lock4queue.release()
            time.sleep(self._interval)

    def stop(self):
        self.thread_stop = True


def crawl(thread_num, directory, max_depth, pattern, interval, timeout):
    log.debug("now crawling with %d thread_num, %d depth, pattern %s!" % (thread_num, max_depth, pattern))
    ThreadList = []
    for i in range(thread_num):
        MyThread = CrawlThread(i, directory, max_depth, pattern, interval, timeout)
        ThreadList.append(MyThread)
        MyThread.start()
    while True:
        if url_table.url_queue.empty():
            flag = 0
            log.debug("checking all thread status")
            for mythread in ThreadList:
                log.debug("thread-%d status is %d" % (mythread._id, mythread.status))
                if mythread.status == 1:
                    flag = 1
            if flag == 0:
                for mythread in ThreadList:
                    log.debug("stopping thread-%d" % mythread._id)
                    mythread.stop()
                log.info("All job finished")
                break
        time.sleep(1)
