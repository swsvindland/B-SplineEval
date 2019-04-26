#!/usr/bin/env python3

def BSpline_Coef(t, y):
    '''
    The function BSpline_Coef produces the coefficients A0, A1, A2, ..., An+1
    for a spline from a set of knots and y values.
    Args:
        t : list : the list of knots
        y : list : the list of y values
    Returns:
        a : list : the list of coeff
        h : list : the list of h values for the eval function
    '''
    n = len(t)
    a = [0 for _ in range(n+2)] # Used n+2 as the textbook has odd indexing
    h = [0 for _ in range(n+2)] # issues with its pseudocode

    for i in range(1, n):
        h[i] = t[i] - t[i-1]

    h[0] = h[1]
    h[n+1] = h[n]
    s = -1
    g = 2*y[0]
    p = s*g
    q = 2
    for i in range(1, n):
        r = h[i+1] / h[i]
        s = -r * s
        g = -r * g + (r + 1) * y[i]
        p = p + g * s
        q = q + s * s
    
    a[0] = -p / q
    for i in range(1, n+1):
        a[i] = ((h[i-1] + h[i]) * y[i-1] - h[i] * a[i-1]) / h[i-1]
    
    return a, h

def BSpline_Eval(t, a, h, x):
    ''' 
    The function BSpline_Eval takes the data form BSpline_Coeff and then computes
    a value of x that is not greater than the largest knot, and computes it. 
    Args:
        t : list : the list of knots
        a : list : the list of coeff
        h : list : the list of h values
        x : int || float : value to solve for
    Returns:
        f(x) : int || float : the value of the interpolated function at x
    '''
    i = len(t)
    for i in range(len(t)-1, 0, -1):
        # the way this is implemented, it does not allow for larger x values than knots
        # or you get an indexing error
        if x - t[i] >= 0:
            break
    i = i + 1
    d = (a[i+1] * (x - t[i-1]) + a[i] * (t[i] - x + h[i+1])) / (h[i] + h[i+1])
    e = (a[i] * (x - t[i-1] + h[i-1]) + a[i-1] * (t[i-1] - x + h[i])) / (h[i-1] + h[i])
    return (d * (x - t[i-1]) + e * (t[i] - x)) / h[i]

def main():
    t = [0.0, 0.6, 1.5, 1.7, 1.9, 2.1, 2.3, 2.6, 2.8, 3.0, 3.6, 4.7, 5.2, 5.7, 5.8, 6.0, 6.4, 6.9, 7.6, 8.0]
    y = [-0.8, -0.34, 0.59, 0.59, 0.23, 0.1, 0.28, 1.03, 1.5, 1.44, 0.74, -0.82, -1.27, -0.92, -0.92, -1.04, -0.79, -0.06, 1.0, 0.0]
    
    a, h = BSpline_Coef(t, y)

    print('For the dataset:')
    print('x: ', t)
    print('y: ', y)
    print('The coefficents for the BSpline are: ')
    print(a)
    print('We can then interpolate a x-value less than 0.0:')
    print('x={}, f(x)={}'.format(-1, BSpline_Eval(t, a, h, -1)))
    print('We can then interpolate a x-value between 0.0 and 8.0:')
    print('x={}, f(x)={}'.format(3.3345, BSpline_Eval(t, a, h, 3.3345)))
    print('However we cannot interpolate a x-value greater or equal to 8:')
    try:
        print('x={}, f(x)={}'.format(8.0, BSpline_Eval(t, a, h, 8.0)))
    except:
        print('x={}, f(x)=Indexing Error'.format(8.0))

if __name__ == '__main__':
    main()
