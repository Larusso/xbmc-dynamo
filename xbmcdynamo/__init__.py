__all__ = ["publish", "generate", "git"]

import argparse
import xbmcdynamo

def _generate(args):
	xbmcdynamo.generate(".", "dist")

def _add_addon(args):
	pass

def _publish(args):
	xbmcdynamo.publish()

def execute_from_command_line(args=None):
	commandParser = argparse.ArgumentParser(description='XBMC repo creator', prog='xbmcdynamo')
	commandParser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

	subparsers = commandParser.add_subparsers(help='sub-command help',dest='command_id')

	generate_parser = subparsers.add_parser('generate', help='generate xbmc addons repository for distribution')
	generate_parser.set_defaults(execute=_generate)

	publish_parser = subparsers.add_parser('publish', help='publish repository')
	publish_parser.set_defaults(execute=_publish)

	add_addon_parser = subparsers.add_parser('add', help='add addon to repository')
	add_addon_parser.set_defaults(execute=_add_addon)

	args = commandParser.parse_args(args)

	if 'execute' not in args:
		commandParser.print_help()

	args.execute(args)