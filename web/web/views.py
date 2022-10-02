# -*- coding: utf-8 -*-
import time
from django.shortcuts import HttpResponse

import uwsgi_bind_vector

from pathlib import Path

def test(request):
	return HttpResponse("Keep hitting Refresh and check for the uwsgi stack trace")
