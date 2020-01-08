import requests
import string
import time
import math

METHOD = 'POST'
BASE_PATH = "http://localhost/sqli-labs-php7/Less-15/?id="
chars = list(string.printable) + [' ']
chars.remove('#')