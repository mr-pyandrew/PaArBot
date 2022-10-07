import datetime
import os

from django.contrib import admin
import json

from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core import serializers
from django.db.models import Count, Sum, Min, Max, F
from django.http import HttpResponse
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models.functions import Trunc
from django.db.models import DateField

from .management.commands import constants

from openpyxl import load_workbook, Workbook

from .models import Users, Bearing, Tree, Leaf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


@admin.register(Users)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'user_name', 'first_name')
    fields = ('external_id', 'user_name', 'first_name')


@admin.register(Bearing)
class BearingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price')
    fields = ('title', 'description', 'price', 'photo', 'tree')
    search_fields = ('title', 'tree', 'description')


@admin.register(Leaf)
class LeafAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_menu', 'leaf')
    fields = ('main_menu', 'leaf')
    search_fields = ('leaf',)


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('branch', 'leaf')
    fields = ('branch', 'leaf')
