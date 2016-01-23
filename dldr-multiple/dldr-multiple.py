#!/usr/bin/env python
# encoding: utf-8
"""dldr-multiple
Download programs from dr.dk/tv by supplying multiple links.

Usage:
  dldr-multiple.py --input=FILE [--slug-name] [--output=DIR]
  dldr-multiple.py <url>... [--slug-name] [--output=DIR]
  dldr-multiple.py (-h | --help)
  dldr-multiple.py --version

Options:
  -h --help                              Show this screen.
  --version                              Show version.
  --slug-name                            Use slug as file name.  E.g. "huset-pa-christianshavn-1" instead of "Huset På Christianshavn (1)"
  -i FILE, --input FILE                  File containing links to programs that should be downloaded. Links must be separated by a new line.
  -o DIR, --output=DIR                   Output directory for the downloaded files.
"""
from docopt import docopt
from schema import Schema, Use, And, Or
import os
import subprocess
import re

DR_URL_PATTERN = r"https?:\/\/(www\.)?dr.dk\/tv\/"

def create_command(url, slug_name = False, output_dir = None):
  cmd = "dldr"
  cmd = "{0} --slug-name".format(cmd) if slug_name else cmd
  cmd = "{0} --output \"{1}\"".format(cmd, output_dir) if output_dir else cmd
  cmd = "{0} {1}".format(cmd, url)
  return cmd

def start_download_for_urls(urls, slug_name = False, output_dir = None):
  for url in urls:
    subprocess.call(create_command(url, slug_name, output_dir), shell=True)

def valid_urls(file_path):
  lines = open(file_path).read().splitlines()
  regex = re.compile(DR_URL_PATTERN)
  return [ l for l in lines if regex.search(l) ]

def validate_urls(urls):
  for url in urls:
    if not re.search(DR_URL_PATTERN, url):
      return False
  return True

def run():
  args = docopt(__doc__, version="dldr-multiple 1.0.0")
  s = Schema({
    '--help': bool,
    '--version': bool,
    '--slug-name': bool,
    '--input': Or(os.path.exists, None, error='Input file does not exist.'),
    '--output': Or(os.path.exists, None, error='Output directory does not exist.'),
    '<url>': validate_urls
  })  
  args = s.validate(args)
  if args['--input']:
    urls = valid_urls(args['--input'])
    start_download_for_urls(urls, args['--slug-name'], args['--output'])
  elif args['<url>']:
    start_download_for_urls(args['<url>'], args['--slug-name'], args['--output'])

if __name__ == "__main__":
  run()
