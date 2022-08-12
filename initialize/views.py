from django.db import connections
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
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
from auth_users.decorator import FilePhotoViewFunction
from datetime import datetime
import base64
import json
import time
from re import A
from django.urls import resolve
from urllib import request


def csrf_failure(request, reason=""):
    raise PermissionDenied()


@login_required
def home(request):
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'pages/home.html',
    {
        "arr_ViewFoto": ViewFoto,
    })
