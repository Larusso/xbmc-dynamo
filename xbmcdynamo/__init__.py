__all__ = ["publish", "generate", "git", "core"]

import argparse
import xbmcdynamo
import xbmcdynamo.generate
from xbmcdynamo.core import ConfigurationProxy

def _generate(args):
	print("generate")
	#xbmcdynamo.generate.generate(args.addons_search_path, args.output_path, args.use_branch)

def _add_addon(args):

	pass

def _publish(args):
	print("publish")
	#xbmcdynamo.publish()

def _clean(args):
	print("clean")
	pass

def _default(args):
	"""runs generate, publish and optional clean"""

	_generate(args)
	_publish(args)
	_clean(args)

def execute_from_command_line(args=None):
	configuration = ConfigurationProxy()

	commandParser = argparse.ArgumentParser(description='XBMC repo creator', prog='xbmcdynamo')
	commandParser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

	generator_group = commandParser.add_argument_group('generate', description='repository generator settings')
	configuration.get_generator_config().set_argparse_attributes(generator_group)

	publish_group = commandParser.add_argument_group('publish', description='publish settings')
	configuration.get_publish_config().set_argparse_attributes(publish_group)

	commandParser.set_defaults(execute=_default)

	subparsers = commandParser.add_subparsers(help='sub-command help')

	generate_parser = subparsers.add_parser('generate', help='generate xbmc addons repository for distribution')
	configuration.get_generator_config().set_argparse_attributes(generate_parser)		
	generate_parser.set_defaults(execute=_generate)

	publish_parser = subparsers.add_parser('publish', help='publish repository')
	configuration.get_publish_config().set_argparse_attributes(publish_parser)
	publish_parser.set_defaults(execute=_publish)

	add_addon_parser = subparsers.add_parser('add', help='add addon to repository')
	add_addon_parser.set_defaults(execute=_add_addon)

	arguments = commandParser.parse_args(args[1:])
	arguments.execute(arguments)
