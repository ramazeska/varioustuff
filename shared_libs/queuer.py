import queue

class Queuer:
    '''wrapper for queue'''
    def __init__(self, maxsize=0):
        self.main_q = queue.Queue(maxsize=maxsize)

    def add_to_q(self, item):
        return self.main_q.put(item)

    def get_from_q(self):
        if self.main_q.empty() is False:
            return self.main_q.get()
        return False

    def is_empty(self):
        return self.main_q.empty()

    def task_done(self):
        return self.main_q.task_done()

