#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals
from flask import Response
import hashlib
import hmac
import json
import re
import logging
import os
import requests


ALLOWED_EVENTS = ('pull_request',)


if hasattr(hmac, "compare_digest"):
    compare_digest = hmac.compare_digest
else:
    def compare_digest(a, b):
        return a == b


class GitHubHandler(object):

    def __init__(self, request):
        self.request = request

    def dispatch(self):
        try:
            self._verify_request()
            self._validate_webhook_secret()
            self._extract()
            return Response('Done!', status=200)
        except Exception, message:
            logging.error(message, exc_info=True)
            return Response('Error occured', status=400)

    def _verify_request(self):
        content_type = self.request.headers.get('Content-Type', None)
        if content_type != 'application/json':
            raise Exception('Unsupported Content-Type: {}'.format(content_type))
        event = self._get_event()
        if event is None:
            raise Exception('missing X-GitHub-Event header')

    def _validate_webhook_secret(self):
        key = os.environ['SECRET_KEY']
        data = self.request.get_data()
        signature = "sha1=" + hmac.new(key, data, hashlib.sha1).hexdigest()
        header_signature = self.request.headers.get('X-Hub-Signature', '')
        if not compare_digest(signature, header_signature):
            raise Exception("The provided signature does not match")

    def _extract(self):
        event = self._get_event()
        if event not in ALLOWED_EVENTS:
            raise Exception('Unkown X-GitHub-Event: {}'.format(event))
        data = json.loads(self.request.get_data())
        if event == 'pull_request':
            handler = PullRequest(data)
            handler.handle_payload()

    def _get_event(self):
        return self.request.headers.get('X-GitHub-Event', None)


class Event(object):

    def __init__(self, payload):
        self.payload = payload

    def handle_payload(self):
        raise NotImplementedError


class PullRequest(Event):

    def handle_payload(self):
        action = self.payload['action']
        if action == 'opened':
            title = self.payload['pull_request']['title']
            id_regex = re.compile(r'#(?P<id>\d+)')
            match = id_regex.search(title)
            if match:
                end_point = self.payload['pull_request']['url']
                end_point = os.path.join(end_point, 'comments')
                end_point = end_point.replace('pulls', 'issues')
                headers = {'Authorization': 'token {}'.format(os.environ['ACCESS_TOKEN'])}
                data = json.dumps({
                    "body": "Fixes #{}".format(match.group('id'))
                })
                response = requests.post(end_point, headers=headers, data=data)
                if not response.ok:
                    logging.error(response.text)
                    raise Exception('Error while adding a comment')
