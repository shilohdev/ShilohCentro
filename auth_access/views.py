from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
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
from functions.permissions.decorator import fetchPermissions, savePermissionsFunction
from functions.users.decorator import fetchUsers
from auth_users.decorator import allowPage, error


def csrf_failure(request, reason=""):
    raise PermissionDenied()


#PÁGINA CONCEDER PERMISSÕES
def setPermissionViews(request):
    if allowPage(request, "insert_permission") == False:
        return 0

    searchPermissions = fetchPermissions()
    searchUsers = fetchUsers()
    return render(request, 'pages/access/viewPermission.html', {
        "searchPermissions": searchPermissions,
        "searchUsers": searchUsers
    })


def ApiSavePermissionsViews(request):
    array = savePermissionsFunction(request)
    return JsonResponse(array, safe=False, status=200)

