import threading, queue
from abc import abstractmethod
from threads.exit_notification import ExitNotification

'''
This is the base class for all threading. Has a thread safe blocking 
queue to handle communication 
'''


class WorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.task_queue = queue.Queue()
        self.alive = False

    def run(self):
        self.alive = True
        while self.alive:
            item = self.task_queue.get()
            if isinstance(item, ExitNotification):
                self.alive = False
            else:
                self.do_pending_work(item)

    @abstractmethod
    def do_pending_work(self, item):
        '''
        This method grabs next item in queue to process. Up to user to implement
        how the object being passed to it is used
        @param item: could be any type of object
        @return:
        '''
        print(item)

    def add_task(self, item):
        self.task_queue.put(item)

    def add_priority_task(self, priority_item):
        '''
        Empty the queue,place the priority item at the front and then put the other tasks behind it
        @param priority_item: Item to be added to front of queue
        @return:
        '''
        items_in_queue = []
        while not self.task_queue.empty():
            item = self.task_queue.get()
            items_in_queue.append(item)
        self.task_queue.put(priority_item)
        for item in items_in_queue:
            self.task_queue.put(item)

    def stop_thread(self):
        en = ExitNotification()
        self.add_priority_task(en)
