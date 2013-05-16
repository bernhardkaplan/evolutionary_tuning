import pylab
import numpy as np

def f(x):
#    return x * np.exp(-x / 5.)
#    return -10 * (np.exp(x) - 10)**2

#    tau = .1 * np.pi 
#    tstart = .1 * np.pi
#    tstop = 1.25 * np.pi
#    if x > tstart and x < tstop:
#        f_x = 1 / (1 + np.exp(-((x-3*tau - tstart) / (tau/2))))
#    else:
#        f_x = 0
#    if x >= tstop:
#        f_x = 1 / (1 + np.exp(-((tstop + 3 * tau -x)/(tau/2))))

#    f_x = np.sin(x / (np.pi))**2

#    sigma = 100. / 20
#    mu = 0.
#    peak = (plateau + 1000.)
#    f_x = peak / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (x - mu)**2 / (2 * sigma**2)) + plateau


    plateau = 10. 
    binsize = 20
    mu = 0
    sigma = 200.# * binsize # [ms]
    peak_freq = 20
    f_x = (peak_freq - plateau) * np.exp(- (x - mu)**2 / (2 * sigma**2)) + plateau

#    f_x = 1 - (1 / (1 + x ))
#    f_x = 0.5 * x * np.exp(-500*x)
#    f_x = 1e-3*np.log10(x)+1
#    f_x = -1e2 * x ** 2 + 1e-4
#    f_x = 1e-3 * x * np.exp(-300000*x**2) + 1e-5
#    f_x =  n umpy.exp(-3000000*x**2) + 1e-5
#    f_x =  1 - np.exp(-0.5 * x) + 1
#    f_x =  1 - np.exp(-0.5 * x) + 1

    return f_x

def f2(x):
#    f_x = 1 / (1 + np.exp(-(1. / (x + 0.5))))
#    f_x = 1 - (1 / (1 + x**2))
    a = 1
    b = -1
    c = 5.
    d = 2
    e = 3
    f = -4
    f_x = x * np.exp(np.sin(a * x + b)) * np.cos(c * x + d) * e + f
    return f_x

def f3(x):
    f_x = np.exp(-(1. / (x)))
    return f_x

def f4(x):
    f_x = 1. / np.exp(x)
    return f_x

def gor_func(x, a1, a2, exp):
    return a1 * x**exp + a2

x_start = 0
x_stop = 20.
#x_stop = 2 * np.pi
n_x = 1000.
dx = (x_stop - x_start) / n_x
#dx = 1e-6

x = np.arange(x_start, x_stop, dx)
y = np.zeros(x.size)
y1 = np.zeros(x.size)
y2 = np.zeros(x.size)
y3 = np.zeros(x.size)
y4 = np.zeros(x.size)

#x_min = x_start
#x_max = x_stop
#y_min = 0.008
#y_max = 0.2
#exp = 3
#a = (y_max - y_min) / (x_max**exp - x_min**exp)
#b = y_min - a * x_min**exp 

y = f2(x)

#for i in xrange(x.size):
#    x_val = x_start + i * dx
#    y[i] = gor_func(x_val, a, b, exp)
#    y[i] = f(x_val)
#    y1[i] = f1(x_val)
#    y[i] = f2(x_val)
#    y3[i] = f3(x_val)
#    print x_val
#    y4[i] = f4(x_val)


#print y
pylab.plot(x, y, '.-')
#pylab.plot(x, y, label="1 - (1 / (1 + x))")
#pylab.plot(x, y2, label="1 - (1 / (1 + x**2))")
#pylab.plot(x, y3, label="exp(-(1. / (x))")
# logarithmic x scale
#pylab.xlim((10**(-6), x_stop))
#pylab.semilogx(x,y)
#pylab.legend()
pylab.show()
