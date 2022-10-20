from asyncio import exceptions
from email.policy import default
from multiprocessing.sharedctypes import Array
import numbers
from this import d
from django.db import connections
from django.db.models import query
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, request
from django.template import RequestContext, Template
from django.views.decorators.csrf import ensure_csrf_cookie
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse
from django.contrib import messages
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from datetime import datetime
import base64
import json
import time
from re import A
from django.contrib.auth.models import User
from numpy import empty
from pymysql import NULL
from auth_finances.models import DashPartners_Closing, DashCommerce_Closing, DashInterno_Closing
from functions.connection.models import Connection, Exams, RegisterActions
from functions.general.decorator import convertDate, checkDayMonth, fetchAdministrator 
from django.forms import model_to_dict
from django.conf import settings
from django.core.files.storage import default_storage
import re






