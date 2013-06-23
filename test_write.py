import random
import json
import time

d = {}
for i in xrange(10):
    fn = 'delme_test.dat'
    f = file(fn, 'w')
    d[i] = {}
    for j in xrange(3):
        d[i]['parameter %d' % j] = random.randint(0, 1000)

    json.dump(d, f)
    f.flush()
    print 'flush'
    print d
    time.sleep(2)

