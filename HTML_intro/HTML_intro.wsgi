#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/webApp/portfolio_project/HTML_intro")

from main import app as application
