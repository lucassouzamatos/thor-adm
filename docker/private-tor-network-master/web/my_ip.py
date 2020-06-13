# -*- coding: utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import optparse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200)
        self.end_headers()
        self.wfile.write('{}\n'.format(self.client_address[0]).encode('utf-8'))


def main(args):
    with HTTPServer((args.bind, args.port), SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()


def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-b', '--bind', help='Listen address (default 127.0.0.1)',
                      default='127.0.0.1')
    parser.add_option('-p', '--port', help='Listen port (default 8000)',
                      default=8000, type=int)
    return parser.parse_args()[0]


if __name__ == '__main__':
    main(parse_args())
