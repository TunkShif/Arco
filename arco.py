#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Arco CLI
Usage:
  arco (new | n) -t <title> -g <category> -f <filename>
  arco (generate | g)
  arco -h | --help
  arco -v | --version

Subcommands:
  new                 Create a new blank page
  generate            Generate pages

Options:
  -h, --help          Help information
  -v, --version       Show version
  -g <tag>            Specify the tag
  -t <title>          Specify the new page title
  -f <filename>       Specify the new page filename
"""

import utils
import os
from docopt import docopt


class Config(object):
    def __init__(self):
        self.config_loader = utils.load_configs()
        self.md_path = 'md'
        self.output_path = 'output'
        self.title = self.config_loader['title']
        self.author = self.config_loader['author']
        self.year = self.config_loader['year']
        self.root = self.config_loader['root']


class Generator(object):
    def __init__(self, config):
        self.config = config

    def gen_tag(self):
        tags = {}
        path = self.config.md_path
        for md in os.listdir(path):
            title, tag, _content = utils.load_md(path+'/'+md)
            if tag not in tags.keys():
                tags[tag] = []
            item = []
            item.append(md)
            item.append(title)
            tags[tag].append(item)
        return tags

    def gen_index(self):
        html = utils.read_file('template/index.html')
        title = self.config.title
        root = self.config.root
        year = self.config.year
        author = self.config.author
        tags = self.gen_tag()
        group = []
        for tag, pages in tags.items():
            group.append('## '+tag)
            for page in pages:
                link = r"/%s/%s.html" % (tag, page[0].split('.')[0])
                item = r"- [%s](%s)" % (page[1], link)
                group.append(item)
        raw_links = '\n'.join(group)
        content = utils.gen_html(raw_links)
        html = html.format(title, root, title, content, year, author)
        utils.write_file(html, 'output/index.html')

    def gen_page(self):
        root = self.config.root
        year = self.config.year
        author = self.config.author
        for md in os.listdir('md'):
            title, tag, raw_content = utils.load_md('md/'+md)
            file_name = md.split('.')[0]
            content = utils.gen_html(raw_content)
            html = utils.read_file('template/page.html')
            html = html.format(title, root, root, content, year, author)
            utils.write_file(html, r'output/%s/%s.html' % (tag, file_name))

    def gen_new(self, title, tag, name):
        content = """Title: %s\nTag: %s\n===============\n""" % (title, tag)
        path = self.config.md_path + '/' + name
        utils.write_file(content, path)

    def gen(self):
        self.gen_index()
        self.gen_page()

    def msg(parameter_list):
        print("All Done!")


if __name__ == "__main__":
    args = docopt(__doc__, version='Arco 0.0.1')
    conf = Config()
    generator = Generator(conf)
    if args['new'] or args['n']:
        generator.gen_new(args['-t'], args['-g'], args['-f'])
        generator.msg()
    if args['generate'] or args['g']:
        generator.gen()
        generator.msg()
