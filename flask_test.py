# -*- coding: utf-8 -*-

"""
"""

from collections import OrderedDict
from flask import Flask, request, render_template, session

app = Flask("flask_test")


def get_info():
    session_info = OrderedDict([(k, session.__dict__[k]) for k in sorted(session.__dict__.keys())])
    req_info = OrderedDict([(k, request.__dict__[k]) for k in sorted(request.__dict__.keys())])
    req_env = OrderedDict([(k, request.environ[k]) for k in sorted(request.environ.keys())])
    tables = [
        {"title": "Session Info", "rows": session_info},
        {"title": "Request Info", "rows": req_info},
        {"title": "Request Info 2", "rows": req_env}
    ]
    return tables


@app.route("/")
def get_root():
    return render_template("example.html", tables=get_info())


@app.route("/item/<path:req_item>")
def get_item(req_item=None):
    return render_template("example.html", req_item=req_item, tables=get_info())
