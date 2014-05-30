from sh import git
import sh

class GithubPagesPublisher:
      def __init__( self ):
            self.target_branch = 'gh-pages'

      def publish_site(self):
            tmp_branch = '__dynamo_deploy__'
            detached_branch = None
            
            git.checkout(self.target_branch)
            self._add_and_commit_site('dist')
            git.push('origin', self.target_branch)
            git.checkout('@{-1}')

      def _add_and_commit_site(self, path):
            git_wt = git.bake(work_tree = path)


            git_wt.add('.',ignore_removal=True)
            status = git.st('-s', '-uno', '--porcelain')

            if status:
                  try:
                        message = "Published {0} to Github.".format(self.target_branch)
                        git_wt.commit(m=message)
                  except sh.ErrorReturnCode_1:
                        print("Can't commit.")
            else:
                  print('no changes to publish')

            git.reset(hard=True)

def publish():
      publisher = GithubPagesPublisher()
      publisher.publish_site()
