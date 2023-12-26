import shutil, os
from configparser import ConfigParser

def getWorkbookName(parser):
	workbookName = parser.get('Template Name', 'Template_Name')
	return workbookName;

def main():
	parser = ConfigParser(allow_no_value=True)
	parser.read('config.ini')
	workbookName = getWorkbookName(parser)
	temporaryFolder = 'File_2'
	os.chdir('.')
	os.mkdir(temporaryFolder)
	shutil.copy('./' + workbookName + '.tdsx', './' + temporaryFolder)
	os.chdir('./' + temporaryFolder)
	prevName = workbookName + '.tdsx'
	newName = workbookName + '.zip'
	os.rename(prevName, newName)

	shutil.unpack_archive(workbookName + '.zip', extract_dir='../', format='zip')

main()

