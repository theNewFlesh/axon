// Alex Braun 07.22.2014

// ----------------------------------------------------------------------------
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
// ----------------------------------------------------------------------------

class DG {
  String _cls;
  get cls => _cls;

  var _owner;
  get owner => _owner;

  Map _spec = {};
  get spec => _spec;

  Map _map = {};
  get map => _map;

  get name => _map['name'];

  build(Map spec) {
    _spec        = spec;
    _map['name'] = spec['name'];
  }

  DG(Map spec, [owner]) {
    _cls = 'DG';
    _owner = owner;
    build(spec);
  }
}

class Component extends DG {
  get Node => _owner;

  Component(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

class Node extends DG {
  get type     => _map['type'];
  get null_    => _map['null'];
  get executor => _map['executor'];
  get informer => _map['informer'];
  get ports    => _map['ports'];

  get all_ports {
    Map output = {};
    for (var type in ports) {
      for (var key in type) {
        output[key] = ports[type][key];
      }
    }
    return output;
  }

  get in_ports  => ports['in_ports'];
  get out_ports => ports['out_ports'];
  get packages  => _map['packages'];

  get all_packages {
    Map output = {};
    for (var type in packages) {
      for (var name in type) {
        output[name] = packages[type][name];
      }
    }
    return output;
  }

  get standard_packages  => _map['packages']['standard'];
  get source_packages    => _map['packages']['source'];
  get generator_packages => _map['packages']['generator'];
  get target_packages    => _map['packages']['target'];
  get instruments        => _map['instruments'];

  void build(Map spec) {
    _spec = spec;
    _map['name']     = spec['name'];
    _map['type']     = spec['type'];
    _map['null']     = spec['null'];
    _map['executor'] = spec['executor'];
    _map['informer'] = spec['informer'];
    _map['ports']    = spec['ports'];
    _map['packages'] = spec['packages'];
  }

  Node(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

class Executor extends Component {
  build(Map spec) {
    _spec = spec;
    _map['name'] = spec['name'];
  }

  Executor(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

class Informer extends Component {
  get state       => _map['state'];
  get logs        => _map['logs'];
  get master_log  => logs['master'];

  get active_logs {
    List output = [];
    for (var log in logs) {
      if (log['state'] == 'active') {
        output.add(log);
      }
    }
    return output;
  }

  get inactive_logs {
    List output = [];
    for (var log in logs) {
      if (log['state'] == 'inactive') {
        output.add(log);
      }
    }
    return output;
  }

  build(Map spec) {
    _spec = spec;
    _map['name']  = spec['name'];
    _map['state'] = spec['state'];
    _map['logs']  = spec['logs'];
  }

  Informer(Map spec, [owner]) : super(spec, owner);
}

class NodeInformer extends Informer {
  get executor_log    => logs['executor'];
  get ports_log       => logs['ports'];
  get instruments_log => logs['instruments'];

  NodeInformer(Map spec, [owner]) : super(spec, owner);
}

class SceneInformer extends Informer {
  get sources_log => logs['sources'];
  get nodes_log   => logs['nodes'];

  SceneInformer(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

class Instrument extends Component {
  get package_name => _map['package_name'];
  get method_name  => _map['method_name'];
  get args         => _map['args'];
  get kwargs       => _map['kwargs'];

  build(Map spec) {
    _spec = spec;
    _map['name']         = spec['name'];
    _map['package_name'] = spec['package_name'];
    _map['name']         = spec['name'];
    _map['method_name']  = spec['method_name'];
    _map['args']         = spec['args'];
    _map['kwargs']       = spec['kwargs'];
  }

  Instrument(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

class Package extends Component {
  get class_       => _map['class'];
  get instance     => _map['instance'];
  get init_args    => _map['init_args'];
  get init_kwargs  => _map['init_kwargs'];
  get methods      => _map['methods'];
  get data         => _map['data'];

  build(Map spec) {
    _spec = spec;
    _map['name']         = spec['name'];
    _map['type']         = spec['type'];
    _map['class']        = spec['class'];
    _map['init_args']    = spec['init_args'];
    _map['init_kwargs']  = spec['init_kwargs'];
    _map['data']         = spec['data'];
    _map['instance']     = spec['instance'];
    _map['methods']      = spec['methods'];
  }

  Package(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

class InPort extends Component {
  get type           => _map['type'];
  get package_name   => _map['package_name'];
  get connected_port => _map['connected_port'];
  get state          => _map['state'];

  build(Map spec) {
    _spec = spec;
    _map['name']           = spec['name'];
    _map['type']           = spec['type'];
    _map['package_name']   = spec['package_name'];
    _map['connected_port'] = spec['connected_port'];
    _map['state']          = spec['state'];
  }

  InPort(Map spec, [owner]) : super(spec, owner);
}

class OutPort extends Component {
  get type            => _map['type'];
  get package_name    => _map['package_name'];
  get connected_ports => _map['connected_ports'];

  build(Map spec) {
    _spec = spec;
    _map['name']            = spec['name'];
    _map['type']            = spec['type'];
    _map['package_name']    = spec['package_name'];
    _map['connected_ports'] = spec['connected_ports'];
  }

  OutPort(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

class Scene extends DG {
  get informer => _map['informer'];
  get sources  => _map['sources'];
  get nodes    => _map['nodes'];

  build(Map spec) {
    _spec = spec;
    _map['name']     = spec['name'];
    _map['informer'] = spec['informer'];
    _map['sources']  = spec['sources'];
    _map['nodes']    = spec['nodes'];
  }

  Scene(Map spec, [owner]) : super(spec, owner);
}
// ----------------------------------------------------------------------------

void main() {
  Map spec = {'name': 'node1', 'executor': 'exec', 'informer': 'info', 'ports': 'ports'};
  var x = new Node(spec);
  print(x.spec);
  print(x.map);
  print(x.name);
  print(x.executor);
  print(x.owner);
}