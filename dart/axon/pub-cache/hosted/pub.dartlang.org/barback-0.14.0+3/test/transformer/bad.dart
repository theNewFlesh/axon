// Copyright (c) 2013, the Dart project authors.  Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

library barback.test.transformer.bad;

import 'package:barback/barback.dart';

import 'mock.dart';

/// A transformer that throws an exception when run, after generating the
/// given outputs.
class BadTransformer extends MockTransformer {
  /// The error it throws.
  static const ERROR = "I am a bad transformer!";

  /// The list of asset names that it should output.
  final List<String> outputs;

  BadTransformer(this.outputs);

  bool doIsPrimary(AssetId id) => true;

  void doApply(Transform transform) {
    // Create the outputs first.
    for (var output in outputs) {
      var id = new AssetId.parse(output);
      transform.addOutput(new Asset.fromString(id, output));
    }

    // Then fail.
    throw ERROR;
  }
}
