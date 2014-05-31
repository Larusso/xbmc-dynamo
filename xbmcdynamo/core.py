
class ConfigurationProxy(object):
    """docstring for ConfigurationProxy"""
    def __init__(self):
        super(ConfigurationProxy, self).__init__()

        self.generator_config = GenerateConfig()
        self.publish_config = PublishConfig()

    def get_generator_config(self):
        return self.generator_config

    def get_publish_config(self):
        return self.publish_config

    def __repr__(self):
        return "ConfigurationProxy(%r)" % "bla"

class GenerateConfig(object):
    """docstring for GenerateConfig"""

    output_path = "dist"
    addons_search_path = "."
    use_branch = False

    def __init__(self):
        super(GenerateConfig, self).__init__()

    def set_argparse_attributes(self, parser):
        parser.add_argument('--addons-search-path', '-asp', type=str, default=".", help="path to folder with xbmc addons")
        parser.add_argument('--use-branch', '-b', action='store_true', help="use current branch name in output path to repository")
        parser.add_argument('--output-path', '-o', type=str, default="dist", help="the output directory")
        
class PublishConfig(object):
    """docstring for PublishConfig"""

    publish_branch = 'gh-pages'
    publish_remote = 'origin'
    cleanup = False

    def __init__(self):
        super(PublishConfig, self).__init__()

    def set_argparse_attributes(self, parser):
        parser.add_argument('--publish-branch', type=str, default='gh-pages', help='branch to publish to')
        parser.add_argument('--publish-remote', type=str, default='origin', help='remote to push to')
        parser.add_argument('--cleanup', '-c', action='store_true', help='cleanup working copy and delete artefacts')
