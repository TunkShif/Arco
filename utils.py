#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import json
import markdown


def mkdir(path):
    os.makedirs(path)


def write_file(content, file):
    path = os.path.split(file)[0]
    if not os.path.isdir(path):
        mkdir(path)
    with open(file, 'wt') as f:
        f.write(content)


def read_file(file):
    with open(file, 'r') as f:
        return f.read()


def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


def load_configs():
    file = "config.json"
    configs = load_json(file)
    return configs


def load_md(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        title = lines[0].split('Title: ')[1].strip()
        tag = lines[1].split('Tag: ')[1].strip()
        content = ''.join(lines[3:])
        return title, tag, content


def copy_theme():
    if not sys.platform == 'linux':
        print('Windows not supported!\nPlease copy css folder manually.')
    else:
        os.system('cp -r  ./template/static/ ./output/')


def gen_html(src):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
            'markdown.extensions.tables', 'markdown.extensions.toc']
    html = markdown.markdown(src, extensions=exts)
    return html
