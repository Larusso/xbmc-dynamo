from sh import git

class GithubPagesPublisher:
	def __init__( self ):
		self.target_branch = 'gh-pages'

	def publish_site(self):
		tmp_branch = '__dynamo_deploy__'
		detached_branch = None
		original_branch = str(git('symbolic-ref', '--short', '-q', 'HEAD').strip())
		print(original_branch)

		git.checkout(self.target_branch)

		self._add_and_commit_site('dist')

		#git.push('origin', self.target_branch)

		#git.checkout('master')

      #   # detect a detached state
      #   # values include (no branch), (detached from x), etc
      #   if original_branch.start_with? '('
      #     detached_branch = git.log(1).first.sha
      #     git.branch(original_branch = tmp_branch).checkout
      #   end

      #   # work in a branch, then revert to current branch
      #   git.branch(@branch).checkout
      #   add_and_commit_site @site_path
      #   git.push(@repo, @branch)

      #   if detached_branch
      #     git.checkout detached_branch
      #     git.branch(original_branch).delete
      #   else
      #     git.checkout original_branch
      #   end
      # end

	def _add_and_commit_site(self, path):
		git('--work-tree',path,'add','.','--ignore-removal')
		
      #   git.with_working(path) do
      #     git.add(".")
      #     begin
      #       git.commit("Published #{@branch} to GitHub pages.")
      #     rescue ::Git::GitExecuteError => e
      #       ExceptionHelper.log_message "Can't commit. #{e}."
      #       ExceptionHelper.mark_failed
      #     end
      #   end
      #   git.reset_hard
      # end

def publish():
	publisher = GithubPagesPublisher()
	publisher.publish_site()
