part of test_bot;

class TestRgbColor {
  static void run() {
    group('RgbColor', () {
      test('Equals', _testEquals);
      test('Invalid', _testInvalid);
      test('HslColor round-trip', _testHslRoundTrip);
      test('Hex round-trip', _testHexRoundTrip);
      test('fromHex', _testFromHex);
      test('invalid hex', _testInvalidHex);
    });
  }

  static void _testEquals() {
    var a = new RgbColor(0, 1, 255);

    expect(a, equals(a));
    expect(a, same(a));

    var b = new RgbColor(0, 1, 255);
    expect(b, equals(a));
    expect(b, isNot(same(a)));

    var c = new RgbColor(1, 2, 3);
    expect(c, isNot(equals(a)));
    expect(c, isNot(same(a)));
  }

  static void _testInvalid() {
    expect(() => new RgbColor(null, 0, 0), throwsArgumentError);
    expect(() => new RgbColor(0, -1, 0), throwsArgumentError);
    expect(() => new RgbColor(0, 0, 256), throwsArgumentError);
  }

  static void _testHslRoundTrip() {
    final colors = _getCoreColors();

    for (final rgb in colors) {
      _expectHslRoundTrip(rgb);
    }

    final hslColors = _getCoreHslColors();
    for (final hsl in hslColors) {
      _expectRgbRoundTrip(hsl);
    }

    for (int i = 0; i < 100; i++) {
      _expectHslRoundTrip(_getRandom());
    }
  }

  static void _testHexRoundTrip() {
    final colors = _getCoreColors();

    for (final rgb in colors) {
      _expectHexRoundTrip(rgb);
    }

    for (int i = 0; i < 100; i++) {
      _expectHexRoundTrip(_getRandom());
    }
  }

  static void _testFromHex() {
    var knownSet = new Map<String, RgbColor>();
    knownSet['#ffffff'] = new RgbColor(255, 255, 255);
    knownSet['#FFFFFF'] = new RgbColor(255, 255, 255);
    knownSet['#000000'] = new RgbColor(0, 0, 0);
    knownSet['#FF0000'] = new RgbColor(255, 0, 0);
    knownSet['#ff0000'] = new RgbColor(255, 0, 0);
    knownSet['#00ff00'] = new RgbColor(0, 255, 0);
    knownSet['#0000ff'] = new RgbColor(0, 0, 255);
    knownSet['#336699'] = new RgbColor(51, 102, 153);

    knownSet.forEach((hex, rgb) {
      var rgb2 = new RgbColor.fromHex(hex);
      expect(rgb2, equals(rgb));
      expect(hex.toLowerCase(), equals(rgb.toHex()));
    });
  }

  static void _testInvalidHex() {
    var badHex = ['aoeu', 'ffffff', 'fff', '#ffffffff', 'white', '', null];
    badHex.forEach((hex) {
      expect(() => new RgbColor.fromHex(hex), throwsArgumentError);
    });
  }

  static List<RgbColor> _getCoreColors() {
    return [
            new RgbColor(0,0,0),
            new RgbColor(1,1,1),
            new RgbColor(42,29,123),
            new RgbColor(42,29,120),
            new RgbColor(254,254,254),
            new RgbColor(255,255,255),
            new RgbColor(245, 255, 193)
            ];
  }

  static List<HslColor> _getCoreHslColors() {
    return [new HslColor(0.0, 1.0, 0.75)];
  }

  static RgbColor _getRandom() {
    return new RgbColor(_randomIntComponent(), _randomIntComponent(), _randomIntComponent());
  }

  static int _randomIntComponent() => rnd.nextInt(256);

  static void _expectRgbRoundTrip(HslColor hsl) {
    final rgb = hsl.toRgb();
    final hsl2 = rgb.toHsl();
    expect(hsl2.h, closeTo(hsl.h, 0.001));
    expect(hsl2.s, closeTo(hsl.s, 0.001));
    expect(hsl2.l, closeTo(hsl.l, 0.001));
  }

  static void _expectHslRoundTrip(RgbColor rgb) {
    final hsl = rgb.toHsl();
    final rgb2 = hsl.toRgb();
    expect(rgb2, equals(rgb));
  }

  static void _expectHexRoundTrip(RgbColor rgb) {
    final hex = rgb.toHex();
    final rgb2 = new RgbColor.fromHex(hex);
    expect(rgb2, equals(rgb));
  }
}
