"""Wrap each app.html (written as an Artifact page body) into a full index.html for GitHub Pages: the root site and schaak/."""
import os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
head = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{name}">
<link rel="apple-touch-icon" href="{icon}">
<link rel="icon" href="{icon}">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
for folder, name, icon in [('', 'Pokéwereld', 'img/25.png'), ('schaak', 'Schaken', '../img/25.png')]:
    d = os.path.join(root, folder)
    body = open(os.path.join(d, 'app.html'), encoding='utf-8').read()
    page = head.replace('{name}', name).replace('{icon}', icon)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page + body + "\n</body>\n</html>\n")
    print(os.path.join(folder, 'index.html'), 'written')
