import sh

def lo():
	return 'Manne'

def current_branch():
	branch = git('symbolic-ref', '--short', '-q', 'HEAD')
	if branch:
		branch = branch.strip()
	return branch