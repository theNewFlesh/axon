#! /usr/bin/env python

# Alex Braun 11.13.2013
# >> INSERT LICENSE HERE <<

'''
.. module:: node_generator
	:date: 11.13.2013
	:platform: Unix
	:synopsis: Axon node generator
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from __future__ import with_statement
import re
import os
# ------------------------------------------------------------------------------

NODE_TEMPLATE = '/Users/alexbraun/Google Drive/code/python/Axon/Utilities/node_template.txt'
NODE_DIRECTORY = '/Users/alexbraun/Google Drive/code/python/Axon/DependencyGraph/Nodes'

class NodeGenerator():
	def generate_node(self, node_base_name='', method_name='', package_name='', import_strings=[]):
		output = ''

		node_base_name_re = re.compile('<node_base_name>')
		import_strings_re = re.compile('<import_strings>')
		package_name_re = re.compile('<package_name>')
		method_name_re = re.compile('<method_name>')

		import_strs = ''
		for item in import_strings:
			import_strs += item + '\n'

		import_strs = import_strs[:-1]

		with open(NODE_TEMPLATE, 'r') as node_template: 
			for line in node_template.readlines():
				new_line = line

				node_base_name_found = node_base_name_re.search(new_line)
				if node_base_name_found:
					new_line = re.sub('<node_base_name>', node_base_name, new_line)

				import_strings_found = import_strings_re.search(new_line) 
				if import_strings_found:
					new_line = re.sub('<import_strings>', import_strs, new_line)

				package_name_found = package_name_re.search(new_line)
				if package_name_found:
					new_line = re.sub('<package_name>', package_name, new_line)
				
				method_name_found = method_name_re.search(new_line)
				if method_name_found:
					new_line = re.sub('<method_name>', method_name, new_line)

				output += new_line
		return output

	def generate_nodes(self, master_argument_index):
		for item in master_argument_index:
			output = self.generate_node(node_base_name=item[0], method_name=item[1], package_name=item[2], import_strings=item[3])
			
			file_name = item[0] + 'Node.py'
			full_path = os.path.join(NODE_DIRECTORY, file_name)
			with open(full_path, 'w') as newFile:
				newFile.write(output)