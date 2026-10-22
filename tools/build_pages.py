"""Wrap app.html (written as an Artifact page body) into a full index.html for GitHub Pages."""
import os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
body = open(os.path.join(root, 'app.html'), encoding='utf-8').read()
head = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Pokéwereld">
<link rel="apple-touch-icon" href="img/25.png">
<link rel="icon" href="img/25.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(head + body + "\n</body>\n</html>\n")
print('index.html written')
