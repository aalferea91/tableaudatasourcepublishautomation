import sys, datetime, xml.etree.cElementTree as ET, codecs
from configparser import ConfigParser


def getWorkbookName(parser):
	workbookName = parser.get('Template Name', 'Template_Name')
	return workbookName;


def getProjectPrefix(parser):
	projectPrefix = parser.get('Project_prefix', 'Project_prefix')
	return projectPrefix;


def getTree(xmlName):
	tree = ET.ElementTree(file=xmlName)
	return tree;


def getRoot(tree):
	root = tree.getroot()
	return root;


def getDatasources(root):
	datasources = root.find("datasources")
	return datasources;


def getDashboards(root):
	dashboards = root.find("dashboards")
	return dashboards;


def getActions(root):
	actions = root.find("actions")
	return actions;


def getSharedViews(root):
	sharedViews = root.find("shared-views")
	return sharedViews;




def getListOfCountries(parser):
	listOfCountries = parser.options('Python List Of Countries')
	for i in range(len(listOfCountries)):
		listOfCountries[i] = listOfCountries[i].upper()
	return listOfCountries;



def datasourcesProcessing(tree, country):
	for i in tree:
		if i.tag == "datasource-dependencies":
			i[0].set("value", '"' + country + '"')
			i[0][0].set("formula", '"' + country + '"')

	return;


def createWorkbook(country, tree, projectPrefix):
	outFileName = 'File_1/' + projectPrefix + '_' + country + '.tds'
	outFile = open(outFileName, 'wb')
	tree.write(outFile)
	print("Created " + outFileName)
	return;


def createCountryWorkbook(countries, now, parser, projectPrefix,  workbook):
	for country in countries:

		tree = getTree(workbook)
		root = getRoot(tree)
		datasources = getDatasources(tree)
		datasourcesProcessing(root, country)
		createWorkbook(country, tree, projectPrefix)


def main():
	parser = ConfigParser(allow_no_value=True)
	parser.read('config.ini')
	ET.register_namespace('user', "http://www.tableausoftware.com/xml/user")
	countries = getListOfCountries(parser)
	workbookName = getWorkbookName(parser)
	projectPrefix = getProjectPrefix(parser)
	workbook = workbookName + ".tds"
	now = datetime.datetime.now()

	createCountryWorkbook(countries, now, parser, projectPrefix,  workbook)


main()
