#!/usr/bin/env python

import argparse
import dynamo

from dynamo.generate import generate
from dynamo.publish import publish

def generate(args):
	dynamo.generate.generate(".", "dist")

def add_addon(args):
	pass

def publish(args):
	dynamo.publish.publish()

commandParser = argparse.ArgumentParser(description='XBMC repo creator', prog='xbmc_repo')
commandParser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

subparsers = commandParser.add_subparsers(help='sub-command help',dest='command_id')

generate_parser = subparsers.add_parser('generate', help='generate xmc addons repository')
generate_parser.set_defaults(execute=generate)

publish_parser = subparsers.add_parser('publish', help='publish repository')
publish_parser.set_defaults(execute=publish)

add_addon_parser = subparsers.add_parser('add', help='add addon to repository')
add_addon_parser.set_defaults(execute=add_addon)

args = commandParser.parse_args()

if 'execute' not in args:
	commandParser.print_help()

print(args)
args.execute(args)