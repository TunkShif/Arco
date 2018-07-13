#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Arco CLI
Usage:
  arco (new | n) -t <title> -g <category> -f <filename>
  arco (generate | g)
  arco (deploy | d)
  arco -h | --help
  arco -v | --version

Subcommands:
  new                 Create a new blank page
  generate            Generate pages
  deploy              Deployment for github

Options:
  -h, --help          Help information
  -v, --version       Show version
  -g <tag>            Specify the tag
  -t <title>          Specify the new page title
  -f <filename>       Specify the new page filename
"""
import os
import json
import markdown
from docopt import docopt


class Utils(object):
    def mkdir(self, path):
        "Create a folder"
        os.mkdir(path)
        print(f'INFO: Folder {path} created!')

    def read_file(self, file):
        "Return the content of a text file"
        with open(file, 'r') as f:
            return f.read()

    def write_file(self, file, content):
        "Write text to a file"
        path = os.path.split(file)[0]  # split file path
        if path is not '':  # if the folder do not exist, then create it
            is_direction = os.path.isdir(path)
            if not is_direction:
                self.mkdir(path)
        with open(file, 'wt') as f:
            f.write(content)
            print(f"INFO: File {file} modified!")

    def gen_html(self, src):
        "Return html generated from markdown"
        exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
                'markdown.extensions.tables', 'markdown.extensions.toc',
                'markdown.extensions.footnotes']
        html = markdown.markdown(src, extensions=exts)
        return html


class Arco(object):
    def __init__(self, utils):
        self.utils = utils
        self.config = self.load_config()

    def load_config(self):
        "Load 'config.json' then return a dict"
        raw = self.utils.read_file('config.json')
        data = json.loads(raw)
        print('INFO: Config loaded!')
        return data

    def new_page(self, title, tag, file):
        "Generate a new markdown page"
        text = f"TITLE: {title}\nTAG: {tag}\n"
        self.utils.write_file(f'markdown/{file}', text)

    def load_md(self, file):
        "Return the title and tag of a markdown file"
        with open(file, 'r') as f:
            lines = f.readlines()  # split title and tag
            title = lines[0].split("TITLE: ")[1].strip()
            tag = lines[1].split("TAG: ")[1].strip()
            content = ''.join(lines[2:])
            return title, tag, content

    def gen_tag_list(self):
        "Return a tag list with markdown file and each one's title"
        tags = {}
        for md in os.listdir('markdown'):
            title, tag, _ = self.load_md(f'markdown/{md}')
            if tag not in tags.keys():
                tags[tag] = []
            item = []
            item.append(md)
            item.append(title)
            tags[tag].append(item)
        return tags

    def gen_page(self):
        "Generate html from each markdown file"
        root = self.config['root']
        year = self.config['year']
        author = self.config['author']
        url = self.config['url']
        if 'blog' not in os.listdir():
            self.utils.mkdir('blog')
        for md in os.listdir('markdown'):
            title, tag, raw_content = self.load_md(f'markdown/{md}')
            file_name = md.split('.')[0]
            content = self.utils.gen_html(raw_content)
            html = utils.read_file('template/page.html')
            html = html.format(title, root, root, content, url, year, author)
            self.utils.write_file(f'blog/{tag}/{file_name}.html', html)
            print(f'INFO: File {file_name}.html generated!')

    def gen_index(self):
        html = self.utils.read_file('template/index.html')
        title = self.config['title']
        root = self.config['root']
        year = self.config['year']
        author = self.config['author']
        tags = self.gen_tag_list()
        group = []
        for tag, pages in tags.items():
            group.append('## '+tag)
            for page in pages:
                link = r"%s%s/%s.html" % (root, tag, page[0].split('.')[0])
                item = r"- [%s](%s)" % (page[1], link)
                group.append(item)
        raw_links = '\n'.join(group)
        content = self.utils.gen_html(raw_links)
        html = html.format(title, root, title, content, year, author)
        self.utils.write_file('blog/index.html', html)
        print('INFO: File index.html generated!')


if __name__ == "__main__":
    args = docopt(__doc__, version='Arco b0.2')
    utils = Utils()
    arco = Arco(utils)
    if args['new'] or args['n']:
        arco.new_page(args['-t'], args['-g'], args['-f'])
    if args['generate'] or args['g']:
        arco.gen_page()
        arco.gen_index()
        os.system('cp -r ./template/static/ ./blog/')
