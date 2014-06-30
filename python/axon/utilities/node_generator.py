#! /usr/bin/env python
# Alex Braun 06.30.2014

# ------------------------------------------------------------------------------
# The MIT License (MIT)

# Copyright (c) 2014 Alex Braun

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

'''
.. module:: node_generator
	:date: 06.30.2014
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