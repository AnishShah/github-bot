#!/usr/bin/env python
# coding=utf-8
from flask import Flask
from flask import request
from handlers import GitHubHandler


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_github_payload():
    # check content type
    handler = GitHubHandler(request)
    return handler.dispatch()


if __name__ == '__main__':
    app.run()
