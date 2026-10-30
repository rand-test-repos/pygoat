import os
import tempfile
import tarfile
import zipfile

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import FileResponse, Http404, HttpResponse, HttpResponseBadRequest

EXPORT_DIR = os.path.join(settings.BASE_DIR, "exports")


export_access_required = permission_required("auth.view_user", raise_exception=True)


@export_access_required
def search_users(request):
    name = request.GET.get("name", "")
    rows = User.objects.filter(username__icontains=name).values(
        "id", "username", "email"
    )[:100]
    return HttpResponse(str(list(rows)))


def _export_path(filename):
    if not filename or os.path.isabs(filename):
        raise Http404
    export_dir = os.path.realpath(EXPORT_DIR)
    path = os.path.realpath(os.path.join(export_dir, filename))
    if os.path.commonpath((export_dir, path)) != export_dir or not os.path.isfile(path):
        raise Http404
    return path


@export_access_required
def download_export(request):
    return FileResponse(open(_export_path(request.GET.get("file")), "rb"))


@export_access_required
def archive_export(request):
    fmt = request.GET.get("format", "zip").lower()
    if fmt not in {"zip", "tar", "tgz", "tar.gz"}:
        return HttpResponseBadRequest("Unsupported archive format")

    suffix = ".zip" if fmt == "zip" else ".tar.gz" if fmt in {"tgz", "tar.gz"} else ".tar"
    archive = tempfile.NamedTemporaryFile(suffix=suffix)
    try:
        if fmt == "zip":
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
                for root, _, files in os.walk(EXPORT_DIR):
                    for filename in files:
                        path = os.path.join(root, filename)
                        output.write(path, os.path.relpath(path, EXPORT_DIR))
        else:
            mode = "w:gz" if fmt in {"tgz", "tar.gz"} else "w"
            with tarfile.open(fileobj=archive, mode=mode) as output:
                output.add(EXPORT_DIR, arcname=os.path.basename(EXPORT_DIR))
        archive.seek(0)
        return FileResponse(archive, as_attachment=True, filename="exports" + suffix)
    except Exception:
        archive.close()
        raise
