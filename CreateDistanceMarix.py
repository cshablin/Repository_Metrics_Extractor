
import os
import xml.etree.ElementTree as ET
import json

raw_jpeek_results_path = '.\\data\\jpeek_metric_files'
extarcted_matrix__lib_path = 'C:\\temp\\extracted_matrix'
maven_test_path = 'C:\\Users\\User\diagnosis\maven_data\matrices'
#
if not os.path.exists(extarcted_matrix__lib_path):
	os.mkdir(extarcted_matrix__lib_path)
metric_to_check = 'LCOM5'

def components_from_test(commit, maven_test_path):  # find list of components from libary
# receive json file name and return all the components in it
	full_test_names = os.listdir(maven_test_path)
	comiits_names = [s.split('_')[1] for s in full_test_names]
	current_test_ind = comiits_names.index(commit)

	file_name = os.path.join(maven_test_path, full_test_names[current_test_ind])
	with open(file_name) as json_file:
		data = json.load(json_file)
	componets = [(comp[0],comp[1]) for comp in data["components_names"]]
	return componets

def  find_methods_in_maven(class_name, components):
#given class name  and components - return all componenets belong to the class
	class_name = '.'+class_name+'.'
	return [method[1] for method in components if class_name in method[1]]



def parse_one_lib(file_name):
#parse rraw esults file
# retrun classes with close methods
	tree = ET.parse(file_name)
	root = tree.getroot()
	good_classes = []
	for package in root.iter('package'):
		package_id = package.attrib['id'].lower()
		for c in package.getchildren():
			id = c.attrib['id'].lower()
			value = c.attrib['value']
			if True or float(value)>0.8:
				good_classes.append(id)
	return good_classes




if __name__ == '__main__':
	print("start init diagnoser")

	jpeek_distance_results = {}
	for commit in os.listdir(raw_jpeek_results_path):


		test_components = components_from_test(commit, maven_test_path)
		file_name = os.path.join(raw_jpeek_results_path,commit,metric_to_check + '.xml')
		good_classes = parse_one_lib(file_name)
		all_combinations = []
		components = components_from_test(commit, maven_test_path)
		i=0
		commit_dict_res = {}
		for good_class in good_classes:
			close_methods = find_methods_in_maven(good_class, components)
			if close_methods:
				i+=1
				commit_dict_res[good_class] = {'weight': len(close_methods), 'methods': close_methods}
		print("fibished to  process commit:{}, number of potential classes: {}".format(commit,i))
		jpeek_distance_results[commit] = commit_dict_res

		with open('c:\\temp\\maven_close_classes_results.json', 'w') as fp:
			json.dump(jpeek_distance_results, fp)
