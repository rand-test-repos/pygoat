import os
import sqlite3
import subprocess

from django.http import HttpResponse, FileResponse
from django.conf import settings

EXPORT_DIR = os.path.join(settings.BASE_DIR, "exports")


def search_users(request):
    name = request.GET.get("name", "")
    conn = sqlite3.connect(settings.DATABASES["default"]["NAME"])
    rows = conn.execute(
        "SELECT id, username, email FROM auth_user WHERE username LIKE '%" + name + "%'"
    ).fetchall()
    return HttpResponse(str(rows))


def download_export(request):
    filename = request.GET.get("file")
    return FileResponse(open(os.path.join(EXPORT_DIR, filename), "rb"))


def archive_export(request):
    fmt = request.GET.get("format", "zip")
    out = subprocess.check_output(
        "tar -c%sf - %s" % (fmt, EXPORT_DIR), shell=True
    )
    return HttpResponse(out, content_type="application/octet-stream")
