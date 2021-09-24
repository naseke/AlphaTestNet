import asyncio
from collections import deque

STATUS_NEW = 'NEW'
STATUS_RUNNING = 'RUNNING'
STATUS_FINISHED = 'FINISHED'
STATUS_ERROR = 'ERROR'
STATUS_CANCELLED = "CANCELLED"


def tic_tac():
    print("Tic")
    yield
    print("Tac")
    yield
    return "Boum!"


def spam():
    print("Spam")
    yield
    print("Eggs")
    yield
    print("Bacon")
    yield
    return "SPAM!"


class Task:
    def __init__(self,coro):
        self.coro = coro
        self.name = coro.__name__
        self.status = STATUS_NEW
        self.return_value = None
        self.error_value = None

    def run(self):
        try:
            self.status = STATUS_RUNNING
            next(self.coro)
        except StopIteration as err:
            self.status = STATUS_FINISHED
            self.return_value = err.value
        except Exception as err:
            self.status = STATUS_ERROR
            self.error_value = err.value

    def is_done(self):
        return self.status in {STATUS_FINISHED, STATUS_ERROR}

    def __repr__(self):
        result = ''
        if self.is_done():
            result = " ({!r})".format(self.return_value or self.error_value)

        return "<Task '{}' [{}]{}>".format(self.name, self.status, result)

    def cancel(self):
        if self.is_done():
            # Inutile d'annuler une tâche déjà terminée
            return
        self.status = STATUS_CANCELLED

    def is_cancelled(self):
        return self.status == STATUS_CANCELLED


class Loop:
    def __init__(self):
        self._running = deque()

    def _loop(self):
        task = self._running.popleft()
        task.run()
        if task.is_done():
            print(task)
            return
        if task.is_cancelled():
            print(task)
            return
        self.schedule(task)

    def run_until_empty(self):
        while self._running:
            self._loop()

    def schedule(self, task):
        if not isinstance(task, Task):
            task = Task(task)
        self._running.append(task)
        return task

    def run_until_complete(self, task):
        task = self.schedule(task)
        while not task.is_done():
            self._loop()

    def ensure_future(coro, loop=None):
        if loop is None:
            loop = Loop()
        return loop.schedule(coro)

def main():
    task = Task(tic_tac())
    print(task)
    while not task.is_done():
        task.run()
        print(task)

def main2():
    running_task = deque()
    running_task.append(Task(tic_tac()))
    running_task.append(Task(tic_tac()))
    while running_task:
        task = running_task.popleft()
        task.run()
        if task.is_done():
            print(task)
        else:
            running_task.append(task)


def main3():
    DEFAULT_LOOP = Loop()
    loop = Loop()
    loop.schedule(tic_tac())
    loop.schedule(spam())
    loop.run_until_empty()


if __name__ == "__main__": main3()