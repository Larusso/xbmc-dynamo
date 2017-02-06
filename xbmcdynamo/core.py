from yaml import load, dump, dump_all, Loader, Dumper


class ConfigurationProxy(object):
    """docstring for ConfigurationProxy"""
    def __init__(self):
        super(ConfigurationProxy, self).__init__()

        object.__setattr__(self,'generator_config',GenerateConfig())
        object.__setattr__(self,'publish_config',PublishConfig())

    def dump_config(self, config_path):
        stream = open(config_path, 'w')
        output = dump({'generate_settings': self.generator_config.__dict__, 'publish_settings': self.publish_config.__dict__}, stream, default_flow_style=False)
        stream.close()
        print("dump_config")
        print(self)

    def load_config(self, config_path):
        stream = open(config_path, 'r')
        config = load(stream)

        if 'generate_settings' in config:
            for key in config['generate_settings'].keys():
                self[key] = config['generate_settings'][key]
            #self.generator_config.__dict__ = config['generate_settings']

        if 'publish_settings' in config:
            self.publish_config.__dict__ = config['publish_settings']

        stream.close()

        print("load_config")
        print(self)

    def __repr__(self):
        return "ConfigurationProxy(%r, %r)" % (self.generator_config, self.publish_config)

    def __setitem__(self,key,value):
        self.__setattr__(key, value)

    def __setattr__(self, name, value):
        if name == 'execute' or name == 'config':
            object.__setattr__(self,name,value)
            return

        if name in self.generator_config:
            setattr(self.generator_config, name, value)

        if name in self.publish_config:
            setattr(self.publish_config, name, value)

class GenerateConfig(object):
    """docstring for GenerateConfig"""

    def __contains__(self, item):
        return item in self.__dict__

    def __repr__(self):
        return "GenerateConfig(output_path: %r, addons_search_path: %r, use_branch: %r)" % (self.output_path, self.addons_search_path, self.use_branch)

    def __init__(self):
        super(GenerateConfig, self).__init__()

        self.output_path = "dist"
        self.addons_search_path = "."
        self.use_branch = False

    def set_argparse_attributes(self, parser):
        parser.add_argument('--addons-search-path', '-asp', type=str, default=self.addons_search_path, help="path to folder with xbmc addons")
        parser.add_argument('--use-branch', '-b', action='store_true', help="use current branch name in output path to repository")
        parser.add_argument('--output-path', '-o', type=str, default=self.output_path, help="the output directory")
        
class PublishConfig(object):
    """docstring for PublishConfig"""

    def __contains__(self, item):
        return item in self.__dict__

    def __repr__(self):
        return "PublishConfig(publish_branch: %r, publish_remote: %r, cleanup: %r)" % (self.publish_branch, self.publish_remote, self.cleanup)

    def __init__(self):
        super(PublishConfig, self).__init__()
        
        self.publish_branch = 'gh-pages'
        self.publish_remote = 'origin'
        self.cleanup = False

    def set_argparse_attributes(self, parser):
        parser.add_argument('--publish-branch', type=str, default=self.publish_branch, help='branch to publish to')
        parser.add_argument('--publish-remote', type=str, default=self.publish_remote, help='remote to push to')
        parser.add_argument('--cleanup', '-c', action='store_true', help='cleanup working copy and delete artefacts')
