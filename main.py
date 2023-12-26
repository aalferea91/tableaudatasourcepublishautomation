import subprocess
from configparser import ConfigParser
import datetime
import shutil,os
import time

def getUrl(parser):
	tableauServerUrl = parser.get('Tableau Server url', 'Tableau_Server_Url')
	return tableauServerUrl;

def getSite(parser):
	tableauSite = parser.get('Tableau Site', 'Tableau_Site')
	return tableauSite;

def getScriptName(parser):
	scriptName = parser.get('Script Name', 'Script_Name')
	return scriptName;

def getTemplateName(parser):
	templateName = parser.get('Template Name', 'Template_Name')
	return templateName;

def getTableauTokenName(parser):
	tableauTokenName = parser.get('Tableau Token Name', 'Tableau_token_name')
	return tableauTokenName;

def getTableauTokenValue(parser):
	tableauTokenValue = parser.get('Tableau Token Value', 'Tableau_token_value')
	return tableauTokenValue;

def getTableauServerProject(parser):
	tableauServerProject = parser.get('Tableau Server Project', 'Tableau_server_project')
	return tableauServerProject;

def getTableauServerSite(parser):
	tableauServerSite = parser.get('Tableau Server Site', 'Tableau_server_site')
	return tableauServerSite;

def getSeparateFoldersConfirmation(parser):
	separateFolderConfirmation = parser.get('Separate_folders_confirmation', 'Confirm_if_separate_folders_is_required')
	return separateFolderConfirmation;

def getProjectPrefix(parser):
	projectPrefix = parser.get('Project_prefix', 'Project_prefix')
	return projectPrefix;

def getDataBaseUserName(parser):
	tableauDbUsername = parser.get('Tableau Database Username', 'Tableau_Db_Username')
	return tableauDbUsername;

def getDataBasePassword(parser):
	tableauDbPassword = parser.get('Tableau Database Password', 'Tableau_Db_password')
	return tableauDbPassword;

def getListOfCountries(parser):
	listOfCountries = parser.options('Python List Of Countries')
	return listOfCountries;

def getProjectSuffixConfirmation(parser):
	projectSuffixConfirmation = parser.get('Project Suffix Confirmation 20181005','Project_Suffix_Confirmation_20181005')
	return projectSuffixConfirmation;

def main ():

	batchFileName = 'executableBatch'
	temporaryFolder = 'File_3'
	parser = ConfigParser(allow_no_value=True)
	parser.read('config.ini')
	tableauServerUrl = getUrl(parser)
	tableauSite = getSite(parser)
	scriptName = getScriptName(parser)
	templateName = getTemplateName(parser)
	tableauTokenName = getTableauTokenName(parser)
	tableauTokenValue = getTableauTokenValue(parser)
	tableauServerProject = getTableauServerProject(parser)
	tableauServerSite = getTableauServerSite(parser)
	separateFolderConfirmation = getSeparateFoldersConfirmation(parser)
	projectPrefix = getProjectPrefix(parser)
	projectSuffixConfirmation = getProjectSuffixConfirmation(parser)
	tableauDbUsername = getDataBaseUserName(parser)
	tableauDbPassword = getDataBasePassword(parser)
	listOfCountries = getListOfCountries(parser)
	now = datetime.datetime.now()
	folder = str(now.year) + str(now.month) + str(now.day)


	for i in range(len(listOfCountries)):
		listOfCountries[i] = listOfCountries[i].upper()

	f = open(batchFileName + '.bat', 'r')

	lines = f.readlines()

	lines[4] = 'python ' + scriptName + '.py\n'
	lines[36] = 'del /q ' + templateName + '.tds\n'
	lines[38] = 'tabcmd login -s ' + tableauServerUrl + ' -t ' + tableauSite + ' --token-name ' + tableauTokenName + ' --token-value ' + tableauTokenValue + '\n'
	lines[40] = 'cd .\File_1' + '\n'


	for country in listOfCountries:
		lines.append(
			'tabcmd publish ' + projectPrefix + '_' + country + '.tdsx' + ' -s ' + tableauServerUrl + ' -t ' + tableauSite + ' --token-name ' +
			tableauTokenName + ' --token-value ' + tableauTokenValue + ' -r ' + tableauServerProject + ' -o --tabbed --db-username \"' +
			tableauDbUsername + '\" --db-password \"' + tableauDbPassword + '\" --save-db-password\n')
		lines.append(
			'tabcmd refreshextracts --datasource  ' + projectPrefix + '_' + country + ' -s ' +
			tableauServerUrl + ' -t ' + tableauSite + ' --token-name ' + tableauTokenName + ' --token-value ' + tableauTokenValue + '\n' )
	f.close()

	os.mkdir(temporaryFolder)
	shutil.copy(batchFileName + '.bat', './' + temporaryFolder)

	os.chdir('./' + temporaryFolder)

	prevName = batchFileName + '.bat'
	newName = batchFileName + '_Temporary.bat'
	os.rename(prevName, newName)

	shutil.copy(newName, '../')

	os.chdir('../')
	shutil.rmtree('./' + temporaryFolder)

	f = open(newName, 'w')
	f.writelines(lines)
	f.close()

	f = open(newName, 'a')
	f.write('tabcmd logout\n')
	f.close()

	subprocess.call(newName, shell=True)

	os.remove(newName)

main()
