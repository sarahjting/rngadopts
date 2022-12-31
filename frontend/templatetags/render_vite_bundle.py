# taken from https://gist.github.com/lucianoratamero/7fc9737d24229ea9219f0987272896a2

import os
import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def render_vite_bundle():
    """
    Template tag to render a vite bundle.
    Supposed to only be used in production.
    For development, see other files.
    """

    try:
        fd = open(f"{settings.VITE_APP_DIR}/dist/manifest.json", "r")
        manifest = json.load(fd)
    except:
        raise Exception(
            f"Vite manifest file not found or invalid. Maybe your {settings.VITE_APP_DIR}/dist/manifest.json file is empty?"
        )

    imports_files = "".join(
        [
            f'<script type="module" src="/static/{manifest[file]["file"]}"></script>'
            for file in manifest["index.html"]["imports"]
        ] if "imports" in manifest["index.html"] else []
    )

    return mark_safe(
        "\n".join([
            f"""<script type="module" src="/static/{manifest['index.html']['file']}"></script>""",
            f"""<link rel="stylesheet" type="text/css" href="/static/{manifest['index.html']['css'][0]}" />""" if "css" in manifest["index.html"] else "",
            imports_files
        ])
    )
