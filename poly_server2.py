



from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
# import os, os.path
# from mimetypes import guess_type
# import datetime
import re
# from  tickets import create_ticket
import logging
import json
# from db_util import db_help
# import tickets
# import loans

logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.DEBUG)

def evaluate(x, poly):
    """
    Evaluate the polynomial at the value x.
    poly is a list of coefficients from lowest to highest.

    :param x:     Argument at which to evaluate
    :param poly:  The polynomial coefficients, lowest order to highest
    :return:      The result of evaluating the polynomial at x
    """

    if len(poly) == 0:
        return 0
    else:
        return x*evaluate(x,poly[1:]) + poly[0]


def bisection(a, b, poly, tolerance):
    """
    Assume that poly(a) <= 0 and poly(b) >= 0.
    Modify a and b so that abs(b-a) < tolerance and poly(b) >= 0 and poly(a) <= 0.
    Return (a+b)/2
    :param a: poly(a) <= 0
    :param b: poly(b) >= 0
    :param poly: polynomial coefficients, low order first
    :param tolerance: greater than 0
    :return:  an approximate root of the polynomial
    """
    if evaluate(a, poly) > 0:
        raise Exception("poly(a) must be <= 0")
    if evaluate(b,poly) < 0:
        raise Exception("poly(b) must be >= 0")
    mid = (a+b) / 2
    if abs(b-a) <= tolerance:
        return mid
    else:
        val = evaluate(mid,poly)
        if val <= 0:
            return bisection(mid, b, poly, tolerance)
        else:
            return bisection(a, mid, poly, tolerance)


class RestHandler(BaseHTTPRequestHandler):

    def get_data(self):
        if 'content-length' in self.headers:
            data = self.rfile.read(int(self.headers['content-length'])).decode()
            logging.info("data is " + data)
            return json.loads(data)
        else:
            logging.debug('no content length')
            return {}

    def send_data(self, rtdata):
        self.send_response(200)
        self.send_header("content-type", "application/json")
        rt = json.dumps(rtdata).encode()
        self.send_header('content-length', len(rt))
        self.end_headers()
        self.wfile.write(rt)

    def send_error_message(self, message, status_code = 412):
        self.send_response(status_code)
        self.send_header("content-type", "application/json")
        rt = json.dumps({'error': message}).encode()
        self.send_header('content-length', len(rt))
        self.end_headers()
        self.wfile.write(rt)



    def do_GET(self):
        logging.info("get started")
        logging.info("path: " + self.path)
        # self.send_response(200)
        # self.send_header("content-type", "application/json")

        data = self.get_data()
        logging.debug("data is " + str(data))

        if re.fullmatch("/evaluate", self.path):
            logging.debug("evaluate")
            if 'x' in data and 'poly' in data:
                try:
                    val = evaluate(data['x'], data['poly'])
                    self.send_data(val)
                except Exception as ex:
                    logging.error(ex)
                    self.send_error_message("Error in evaluating polynomial")
            else:
                self.send_error_message("missing data for request")
        elif re.fullmatch("/bisection", self.path):
            logging.debug("bisection")
            if 'a' in data and 'b' in data and 'tol' in data and 'poly' in data:
                try:
                    val = bisection(data['a'], data['b'], data['poly'], data['tol'])
                    self.send_data(val)
                except Exception as ex:
                    logging.error(ex)
                    self.send_error_message("Error in applying bisection to  polynomial")
            else:
                self.send_error_message("missing data for request")
        else:
            self.send_error_message('invalid path')




server_port = 23232


if __name__ == '__main__':
    server_address = ('', server_port)
    httpd = HTTPServer(server_address, RestHandler)
    httpd.serve_forever()