#!/usr/bin/env python
# coding=utf-8
from flask import Flask
from flask import request
from handlers import GitHubHandler
import os

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_github_payload():
    # check content type
    handler = GitHubHandler(request)
    return handler.dispatch()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
