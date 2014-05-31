
class ConfigurationProxy(object):
    """docstring for ConfigurationProxy"""
    def __init__(self):
        super(ConfigurationProxy, self).__init__()

        object.__setattr__(self,'generator_config',GenerateConfig())
        object.__setattr__(self,'publish_config',PublishConfig())

    def get_generator_config(self):
        return self.generator_config

    def get_publish_config(self):
        return self.publish_config

    def __repr__(self):
        return "ConfigurationProxy(%r, %r)" % (self.generator_config, self.publish_config)

    def __setattr__(self, name, value):
        if name == 'execute':
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
        return "output_path: %r, addons_search_path: %r, use_branch: %r" % (self.output_path, self.addons_search_path, self.use_branch)

    def __init__(self):
        super(GenerateConfig, self).__init__()

        self.output_path = "dist"
        self.addons_search_path = "."
        self.use_branch = False

    def set_argparse_attributes(self, parser):
        parser.add_argument('--addons-search-path', '-asp', type=str, default=".", help="path to folder with xbmc addons")
        parser.add_argument('--use-branch', '-b', action='store_true', help="use current branch name in output path to repository")
        parser.add_argument('--output-path', '-o', type=str, default="dist", help="the output directory")
        
class PublishConfig(object):
    """docstring for PublishConfig"""

    def __contains__(self, item):
        return item in self.__dict__

    def __repr__(self):
        return "publish_branch: %r, publish_remote: %r, cleanup: %r" % (self.publish_branch, self.publish_remote, self.cleanup)

    def __init__(self):
        super(PublishConfig, self).__init__()
        self.publish_branch = 'gh-pages'
        self.publish_remote = 'origin'
        self.cleanup = False

    def set_argparse_attributes(self, parser):
        parser.add_argument('--publish-branch', type=str, default='gh-pages', help='branch to publish to')
        parser.add_argument('--publish-remote', type=str, default='origin', help='remote to push to')
        parser.add_argument('--cleanup', '-c', action='store_true', help='cleanup working copy and delete artefacts')
