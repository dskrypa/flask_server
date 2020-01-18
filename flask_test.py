#!/usr/bin/env python3
"""
Example Flask server that displays request information

:author: Doug Skrypa
"""

import argparse
import logging
import socket
import traceback
from collections import OrderedDict

from flask import Flask, request, render_template, session

log = logging.getLogger(__name__)
app = Flask(__name__)


def dict2table(contents):
    if not isinstance(contents, list):
        contents = [contents]

    html = []
    for content in contents:
        if (len(content) == 2) and all(k in content for k in ('title', 'rows')):
            title = content['title']
            rows = content['rows']
            html.append('<h1>{}</h1>'.format(title))
        else:
            rows = content

        html.append('<table>')
        for key, val in rows.items():
            html.append('<tr>')
            html.append('<td>{}</td>'.format(key))
            if isinstance(val, dict):
                html.append('<td>')
                html.extend(dict2table(val))
                html.append('</td>')
            else:
                html.append('<td>{}</td>'.format(val))
            html.append('</tr>')
        html.append('</table>')
    return html


def get_info():
    """
    http://flask.pocoo.org/docs/1.0/api/#flask.Request

    :return:
    """
    skip = {'headers', 'cookies', 'environ'}
    session_attrs = OrderedDict([(k, getattr(session, k)) for k in sorted(dir(session)) if not k.startswith('__')])
    request_attrs = OrderedDict([
        (k, getattr(request, k)) for k in sorted(dir(request)) if not k.startswith('__') and k not in skip
    ])
    headers = OrderedDict([(k, request.headers[k]) for k in sorted(request.headers.keys())])
    cookies = OrderedDict([(k, request.cookies[k]) for k in sorted(request.cookies.keys())])
    req_env = OrderedDict([(k, request.environ[k]) for k in sorted(request.environ.keys())])
    tables = [
        {'title': 'session', 'rows': session_attrs},
        {'title': 'request', 'rows': request_attrs},
        {'title': 'request.headers', 'rows': headers},
        {'title': 'request.cookies', 'rows': cookies},
        {'title': 'request.environ', 'rows': req_env}
    ]
    return tables


@app.route('/')
def get_root():
    return render_template('example.html', pre_rendered=dict2table(get_info()))


@app.route('/item/<path:req_item>')
def get_item(req_item=None):
    return render_template('example.html', req_item=req_item, tables=get_info())


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Test Flask Server')
    parser.add_argument('--use_hostname', '-u', action='store_true', help='Use hostname instead of localhost/127.0.0.1')
    parser.add_argument('--port', '-p', type=int, help='Port to use')
    args = parser.parse_args()

    run_args = {'port': args.port}
    if args.use_hostname:
        run_args['host'] = socket.gethostname()

    try:
        app.run(**run_args)
    except Exception as e:
        log.debug(traceback.format_exc())
        log.error(e)
