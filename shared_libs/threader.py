import threading
from logger import SharedLogger


class Threader(SharedLogger):
    def __init__(self, threadmax=1):
        SharedLogger.__init__(self)
        self.max_threads = threadmax

    def curr_threads_num(self):
        return threading.active_count()


    def bringup_daemon(self, fnc,q):
        try:
            self.src_fnc = fnc
            self.src_q = q
            for i in range(self.max_threads):
                worker = threading.Thread(target=self.worker_do, args=(self.src_fnc, self.src_q, ))
                worker.setDaemon(True)
                worker.start()

        except Exception as e:
            self.log.error('bringup daemon: Caught: {}'.format(e))

    def ensure_done(self):
        for t in threading.enumerate():
            if t.daemon:
                if t.isAlive():
                    self.log_info('{} waiting to join'.format(t.name))
                    t.join(60)
                if t.isAlive() is False:
                    self.log_info('{} done'.format(t.name))


    def worker_do(self, fnc, q):
        while True:
            if self.src_q.empty() is False:
                self.log_info('Checking the q')
                try:
                    item = self.src_q.get()
                    if fnc(item) is True:
                        self.src_q.task_done()

                except Exception as e:
                    self.log.error('Worker: Caught: {}, params: {}'.format(e, item))
                    self.died = True

