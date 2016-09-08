# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest

import codecs
import os
import sys

from selenium import webdriver

from widgetastic.core.browser import Browser


class CustomBrowser(Browser):
    @property
    def product_version(self):
        return '1.0.0'


@pytest.fixture(scope='session')
def selenium(request):
    driver = webdriver.PhantomJS()
    request.addfinalizer(driver.quit)
    driver.maximize_window()
    return driver


@pytest.fixture(scope='function')
def browser(selenium, httpserver, request):
    this_module = sys.modules[__name__]
    path = os.path.dirname(this_module.__file__)
    testfilename = path + '/testing_page.html'
    httpserver.serve_content(codecs.open(testfilename, mode='r', encoding='utf-8').read())
    selenium.get(httpserver.url)
    return CustomBrowser(selenium)
