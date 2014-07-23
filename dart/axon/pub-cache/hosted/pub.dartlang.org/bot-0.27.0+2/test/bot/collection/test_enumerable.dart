part of test_bot;

class TestEnumerable {

  static void run() {
    group('Enumerable', () {
      test('count', _testCount);
      test('distinct', _testDistinct);
      test('exclude', _testExclude);
      test('forEachWithIndex', _testForEachWithIndex);
      group('group', () {
        test('simple', _testSimpleGrouping);
        test('complex', _testComplexGrouping);
      });
      test('selectNumbers', _testSelectNumbers);
      test('toMap', _testToMap);
      test('concat', _testConcat);
    });
  }

  static void _testConcat() {
    final enumValue = $([0, 1, 2]).concat([3, 4, 5]);
    expect(enumValue, orderedEquals([0, 1, 2, 3, 4, 5]));
  }

  static void _testExclude() {
    final enumValue = $([0, 1, 2, 3, 4]);
    expect(enumValue.exclude([]), orderedEquals(enumValue));
    expect(enumValue.exclude([5, -1]), orderedEquals(enumValue));
    expect(enumValue.exclude([1, 3]), orderedEquals([0, 2, 4]));
  }

  static void _testDistinct() {
    final enumValue = $([0, 0, 1, 1, 2, 2, 0, 1, 2, 3, 4, 5]);
    expect(enumValue.distinct(), unorderedEquals([0, 1, 2, 3, 4, 5]));

    final oddsAndEvens = enumValue.distinct((a, b) => a % 2 == b % 2);
    expect(oddsAndEvens, unorderedEquals([0, 1]));
  }

  static void _testForEachWithIndex() {
    final enumValue = $([0, 1, 2, 3]);
    enumValue.forEachWithIndex((e, i) {
      expect(i, equals(e));
    });
  }

  static void _testToMap() {
    final noDupes = $(['the', 'kitty', 'is', 'super']);

    //
    // where the item is the key
    //
    var hashMap = noDupes.toMap((s) => s.length);
    hashMap.forEach((k, v) {
      expect(k.length, equals(v));
    });
    expect(hashMap.keys, unorderedEquals(noDupes));

    //
    // where the key is produced by a func, too
    //
    hashMap = noDupes.toMap((s) => s, (s) => s[0]);
    hashMap.forEach((k, v) {
      expect(k, equals(v[0]));
    });
    expect(hashMap.values, unorderedEquals(noDupes));

    //
    // doesn't support duplicate keys
    //
    expect(() => noDupes.toMap((s) => s, (s) => s.length),
        throwsUnsupportedError);

    final withDupes = $(['the', 'cat', 'is', 'the', 'super', 'cat']);
    expect(() => withDupes.toMap((s) => s.length), throwsUnsupportedError);
  }

  static void _testCount() {
    final e = $([1, 2, 3, 4, 5, 6]);

    expect(e.length, equals(6));

    var count = e.count((x) => x % 2 == 0);
    expect(count, equals(3));
  }

  static void _testSelectNumbers() {
    final e = $(['a', 'cat', 'is', 'super']).selectNumbers((x) => x.length);
    expect(e, orderedEquals([1, 3, 2, 5]));

    final sum = e.sum();
    expect(sum, equals(11));
  }

  static List<String> _getChars(String input) {
    var list = new List<String>();
    for (int i = 0; i < input.length; i++) {
      list.add(input[i]);
    }

    return list;
  }

  //
  // Grouping
  //
  static void _testComplexGrouping() {
    final Func1<String, int> keyFunc = (str) => str.length;

    //
    // Test 1
    //
    var grouping = $(['a']).group(keyFunc);

    expect(grouping.length, equals(1));

    var list = grouping[1];
    expect(list.length, equals(1));
    expect(list[0], equals('a'));

    //
    // Test 2
    //
    final source = ['a', 'b', 'c', 'ab', 'bc', 'abc'];
    grouping = $(source).group(keyFunc);

    expect(grouping.length, equals(3));

    list = grouping[1];
    expect(list.length, equals(3));
    expect(list, contains('a'));
    expect(list, contains('b'));
    expect(list, contains('c'));
    expect(list, isNot(contains('d')));

    list = grouping[2];
    expect(list.length, equals(2));
    expect(list, contains('ab'));
    expect(list, contains('bc'));
    expect(list, isNot(contains('a')));

    list = grouping[3];
    expect(list.length, equals(1));
    expect(list[0], equals('abc'));
    expect(list, isNot(contains('d')));

    list = grouping[0];
    expect(list, isNull);

    // verify all values
    list = new List<String>.from(grouping.getValues());
    expect(list, unorderedEquals(source));
  }

  static void _testSimpleGrouping() {
    //
    // Test 1
    //
    var grouping = $([1]).group();

    expect(grouping.length, equals(1));

    var list = grouping[1];
    expect(list.length, equals(1));
    expect(list[0], equals(1));

    //
    // Test 2
    //
    grouping = $([1, 1]).group();

    expect(grouping.length, equals(1));

    list = grouping[1];
    expect(list.length, equals(2));
    expect(list[0], equals(1));
    expect(list[1], equals(1));

    //
    // Test 3
    //
    grouping = $([1, 2, 3, 1, 2, 1]).group();

    expect(grouping.length, equals(3));

    list = grouping[1];
    expect(list.length, equals(3));
    expect(list, everyElement(equals(1)));

    list = grouping[2];
    expect(list.length, equals(2));
    expect(list, everyElement(equals(2)));

    list = grouping[3];
    expect(list.length, equals(1));
    expect(list, everyElement(equals(3)));

    list = grouping[4];
    expect(list, isNull);
  }
}
