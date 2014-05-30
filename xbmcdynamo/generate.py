import os
import sys
import errno
import xml.dom.minidom
import zipfile
from sh import git
 
def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise

def get_git_branch():
	return git('symbolic-ref', '--short', '-q', 'HEAD').strip()

# Compatibility with 3.0, 3.1 and 3.2 not supporting u"" literals
if sys.version < '3':
	import codecs
	def u(x):
		return codecs.unicode_escape_decode(x)[0]
else:
	def u(x):
		return x

class Generator:
	"""
		Generates a new addons.xml file from each addons addon.xml file
		and a new addons.xml.md5 hash file. Must be run from the root of
		the checked-out repo. Only handles single depth folder structure.
	"""
	def __init__( self, addons_path, output_base_path, use_branch_name=True ):
		# generate files
		if use_branch_name:
			addons_xml_path = "{0}/{1}/addons.xml".format(output_base_path, get_git_branch())
			make_sure_path_exists("{0}/{1}".format(output_base_path, get_git_branch()))
		else:
			addons_xml_path = "{0}/addons.xml".format(output_base_path)
			make_sure_path_exists("{0}".format(output_base_path))

		self._generate_addons_file(addons_path, addons_xml_path)
		self._generate_md5_file(addons_xml_path)
		# notify user
		print("Finished updating addons xml and md5 files")
 
	def _generate_addons_file( self, addons_path, output_path ):
		# addon list
		addons = os.listdir( addons_path )
		# final addons text
		addons_xml = u("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n")
		# loop thru and add each addons addon.xml file
		for addon in addons:
			try:
				# skip any file or .svn folder or .git folder
				if ( not os.path.isdir( addon ) or addon == ".svn" or addon == ".git" ): 
					continue

				# create path
				_path = os.path.join( addon, "addon.xml" )

				# split lines for stripping
				xml_lines = open( _path, "r" ).read().splitlines()

				# new addon
				addon_xml = ""
				# loop thru cleaning each line
				for line in xml_lines:
					# skip encoding format line
					if ( line.find( "<?xml" ) >= 0 ): continue
					# add line
					if sys.version < '3':
						addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
					else:
						addon_xml += line.rstrip() + "\n"
				# we succeeded so add to our final addons.xml text
				addons_xml += addon_xml.rstrip() + "\n\n"
			except Exception as e:
				# missing or poorly formatted addon.xml
				print("Excluding %s for %s" % ( _path, e ))
		# clean and add closing tag
		addons_xml = addons_xml.strip() + u("\n</addons>\n")
		# save file
		self._save_file( addons_xml.encode( "UTF-8" ), file=output_path )
 
	def _generate_md5_file( self, addons_file ):
		# create a new md5 hash
		try:
			import md5
			m = md5.new( open( addons_file, "r" ).read() ).hexdigest()
		except ImportError:
			import hashlib
			m = hashlib.md5( open( addons_file , "r", encoding="UTF-8" ).read().encode( "UTF-8" ) ).hexdigest()
 
		# save file
		try:
			self._save_file( m.encode( "UTF-8" ), file="{0}.md5".format(addons_file) )
		except Exception as e:
			# oops
			print("An error occurred creating addons.xml.md5 file!\n%s" % e)
 
	def _save_file( self, data, file ):
		try:
			# write data to the file (use b for Python 3)
			open( file, "wb" ).write( data )
		except Exception as e:
			# oops
			print("An error occurred saving %s file!\n%s" % ( file, e ))

class Zipper:
	"""
		Creates zip archives for every addon.
	"""
	def __init__( self, addons_file, addons_path, output_base_path, use_branch_name=True ):
		print("Create addon zip archives")
		self.addons = dict()

		if use_branch_name:
			output_path = "{0}/{1}".format(output_base_path, get_git_branch())
			make_sure_path_exists("{0}/{1}".format(output_base_path, get_git_branch()))
		else:
			output_path = "{0}".format(output_base_path)
			make_sure_path_exists("{0}".format(output_base_path))
		
		self._read_addons(addons_file)
		self._zip_addons(output_path)

	def _read_addons(self, addons_file):
		addons = xml.dom.minidom.parse(addons_file).getElementsByTagName("addon")
		for addon in addons:
			version = addon.getAttribute('version')
			addon_id = addon.getAttribute('id')
			self.addons[addon_id] = version

	def _add_dir_to_zip(self, path, zip):
		for dirpath, dirnames, filenames in os.walk(path):
			if '.git' in dirnames:
				dirs.remove('.git')

			if '.svn' in dirnames:
				dirs.remove('.svn')

			for file in filenames:
				zip.write(os.path.join(dirpath, file))

	def _zip_addons(self, output_path):
		for addon_id, version in self.addons.items():
			make_sure_path_exists("{0}/{1}".format(output_path, addon_id))
			print(addon_id,version)
			zipf = zipfile.ZipFile("{0}/{1}/{1}.{2}.zip".format(output_path, addon_id,version), 'w')
			self._add_dir_to_zip(addon_id, zipf)
			zipf.close()


def generate(addons_path, output_base_path, use_branch_name=True ):
	Generator(addons_path, output_base_path)

	if use_branch_name:
		addons_file = "{0}/{1}/addons.xml".format(output_base_path, get_git_branch())
	else:
		addons_file = "{0}/addons.xml".format(output_base_path)
	Zipper(addons_file,addons_path, output_base_path)
