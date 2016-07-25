#!/usr/bin/python3

from http.client import HTTPConnection, HTTPMessage
import json
from poly_server2 import server_port


def sendtoserver(method, url, data):
    h = HTTPConnection('localhost', port=server_port)
    h.request(method, url, json.dumps(data).encode())
    response = h.getresponse()
    r = response.read()
    try:
        answer = float(r)
    except ValueError:
        return "Error Received: " + str(response.status) + ' ' + response.reason + " : " + str(r)
    h.close()
    return answer


def buildrequest(url, data):
    #print (url, data)
    request = ''
    if url == '/bisection':
        request = {'a': data[0], 'b': data[1], 'poly': data[2], 'tol': data[3]}
    elif url == '/evaluate':
        request = {'x': data[0], 'poly': data[1]}
    return request


a = 1.
b = 0.
poly = [851., -3083., 1665., -225.]
tol = 1e-15
BISECTION = '/bisection'
EVALUATE = '/evaluate'

q1 = sendtoserver('GET', BISECTION, buildrequest(BISECTION, [a, b, poly, tol]))
print(q1)

a = sendtoserver('GET', EVALUATE, buildrequest(EVALUATE, [q1, poly]))
print(a)

newA = 2.
newB = 3.
q3 = sendtoserver('GET', BISECTION, buildrequest(BISECTION, [newA, newB, poly, tol]))
print(q3)

q4 = sendtoserver('GET', EVALUATE, buildrequest(EVALUATE, [q3, poly]))
print(q4)

newerA = 5.
newerB = 4.
q5 = sendtoserver('GET', BISECTION, buildrequest(BISECTION, [newerA, newerB, poly, tol]))
print(q5)

q6 = sendtoserver('GET', EVALUATE, buildrequest(EVALUATE, [q5, poly]))
print(q6)

x = 1.2349860923954652
q7 = sendtoserver('GET', EVALUATE, buildrequest(EVALUATE, [x, poly]))
print(q7)

newX = 3.6983472409378684
q8 = sendtoserver('GET', EVALUATE, buildrequest(EVALUATE, [newX, poly]))
print(q8)

newestA = 4.
newestB = 5.
q9 = sendtoserver('GET', BISECTION, buildrequest(BISECTION, [newestA, newestB, poly, tol]))
print(q9)

q10 = sendtoserver('GET', '/eval', buildrequest(EVALUATE, [a, b, poly, tol]))
print(q10)

q11 = sendtoserver('GET', EVALUATE, {'poly': poly})
print(q11)

q12 = sendtoserver('GET', BISECTION, {'a': a, 'poly': poly, 'tol': tol})
print(q12)
