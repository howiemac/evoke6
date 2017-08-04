"""
decorator to make functions that only ever return the first non-false value they create
"""
from datetime import datetime, timedelta
import time


class Cached(object):
    "a decorator"

    def __init__(self, timeout=0, file=''):
        "timeout: int seconds        file='string path to store result'"
        self.result = ''
        self.time = datetime.now()
        self.timeout = timeout
        self.file = file

    def __call__(self, fn):
        "wrap our function"

        def wrapper(*a, **k):
            # regenerate content on finding a recache parameter
            if k.get('recache', 0):
                self.result = ''
                del k['recache']
            if self.timedout():
                self.result = ''
            # regenerate if no content available
            if not self.result:
                self.result = fn(*a, **k)
                self.time = datetime.now()
                if self.file:
                    open(self.file, 'w').write(self.result)
            return self.result

        return wrapper

    def timedout(self):
        "returns True if we have timed out"
        # if there's no timeout we will not regenerate
        if not self.timeout:
            return False
        return datetime.now() >= self.time + timedelta(seconds=self.timeout)


def cached(fn):
    return Cached()(fn)


if __name__ == '__main__':

    @cached
    def fn():
        return datetime.now()

    t1 = fn()
    t2 = fn()
    assert t1 == t2, 'should always return an identical value'
    t3 = fn(recache=True)
    assert t2 != t3, 'should have been recached'

    @Cached(timeout=2)
    def fn2():
        return datetime.now()

    t4 = fn2()
    time.sleep(0.5)
    t5 = fn2()
    assert t4 == t5, 'should not have regenerated yet'
    time.sleep(2)
    t6 = fn2()
    assert t4 != t6, 'should have regenerated by now'

    @Cached(file='/tmp/test.html')
    def fn3():
        return repr(datetime.now())

    t7 = fn3()
    t8 = open('/tmp/test.html').read()
    assert t7 == t8, 'should have sent an identical copy to file'
