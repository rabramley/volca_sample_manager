#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from celery.task.control import inspect
from flask import url_for
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from '.env' file.
load_dotenv()

from vsm import create_app

application = create_app()
application.app_context().push()

from vsm.celery import celery
