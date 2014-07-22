// Alex Braun 07.22.2014

// -----------------------------------------------------------------------------
// The MIT License (MIT)

// Copyright (c) 2014 Alex Braun

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.
// -----------------------------------------------------------------------------

import 'package:polymer/polymer.dart';
import 'package:bwu_datagrid/bwu_datagrid.dart';
import 'package:quiver/iterables.dart';
// -----------------------------------------------------------------------------

class Panel {
	List _index;
	get index => _index;

	Map _index_lut;
	get index_lut => _index_lut;

	List _values;
	get values => _values;

	String _separator  = '__null__';
	get separator => _separator;

	String _index_item = '<-----';
	get index_item => _index_item;

	String _head      = '     |--- ';
	get head => _head;

	String _tail      = ' -------> ';
	get tail => _tail;

	String _branch    = '     |    ';
	get branch => _branch;

	get data => zip(_index, _values);

	get width => _index[0].length + 1;

	get height => _index.length;
	// -------------------------------------------------------------------------

	List nested_map_to_matrix(Map data) {
		sep = _separator;
		List output;
		List _nested_map_to_matrix(Map data, String name) {
			data.forEach(var key, var value) {
				var new_key = name + key.toString();
				if val is Map and val != {} {
					output.add([new_key, _index_item]);
					_nested_map_to_matrix(val, new_key);
				}
				else {
					output.add([new_key, val]);
				}
		_nest
		}
	}

	Map matrix_to_nested_map(List data) {
		List output;
		data.forEach(var row) {
			var keys = row[0];
			var value = row[1];
			var cursor = output;
			keys.forEach(var key) {
				// build map with dummy values
				try {
					cursor = cursor[key]
				}
				on Exception catch(e) {
					if (value != _index_item) {
						cursor[key] = {'__value__': value};
						cursor = cursor[key];
					}
					else {
						cursor[key] = {};
						cursor = cursor[key];
					}
				// replace dummy maps with real values
				cursor = output;
				keys.forEach(var key) {
					if (cursor[key].keys == ['__value__']) {
						var val = cursor[key]['__value__'];
						cursor[key] = val;
					}
					cursor = cursor[key];
					}
				}
				}
			}
		return output;
		}
		}
	}
				}