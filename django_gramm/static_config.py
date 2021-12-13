from django.contrib.staticfiles.apps import StaticFilesConfig


class MyStaticFilesConfig(StaticFilesConfig):
    ignore_patterns = ["canvas-to-blob.min.js", "load-image.all.min.js"]  # your custom ignore list