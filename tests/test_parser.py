import json
import unittest
import pytest
from pytest_mock import mocker
from news_parser import parser


class TestAddGame(unittest.TestCase):
    def test_parser(self):
        news = '{"gid":"1","title":"title","url":"url","is_external_url":true,"author":"author","contents":"contents","feedlabel":"feedlabel","date":1,"feedname":"feedname","feed_type":1,"appid":730,"tags":["patchnotes"]}'

        self.assertEqual(
            parser(json.loads(news)),
            'Game news for counter-strike 2\n<a href ="url">Check full news here</a>\n<b>title</b>\n\n<b>Update date: 1970-01-01 01:00:01</b>\n\n',
        )
