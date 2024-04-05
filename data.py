import os
import sys
import time
#import json
sys.path.append(
    os.path.join(os.path.dirname(__file__), 'groupmesagebot')
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "groupmesagebot.settings")
import django
django.setup()

from django.conf import settings
from django.core.validators import validate_email
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist

from main.models import Report
import datetime
from django.utils import timezone

import requests






def save_report(crypto_address,message,username,userid):
    message = Report(crypto_address=crypto_address, message=message,username=username,userid=userid)
    message.save()

def get_user_rank(userid):
    all_report_count = Report.objects.filter(userid=userid).count()
    #print(all_report_count)
    if all_report_count > 100:
        result = "Snitch King"
    elif all_report_count > 50:
        result = "Osinter"
    elif all_report_count > 10:
        result = "Concerned Civilian"
    else:
        result = "Prison snitch"
    return result