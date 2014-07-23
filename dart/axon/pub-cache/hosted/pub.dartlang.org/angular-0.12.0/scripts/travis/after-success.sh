#!/bin/bash
set -e

echo '*******************'
echo '** AFTER_SUCCESS **'
echo '*******************'


echo '---------------------'
echo '-- WAIT FOR OTHERS --'
echo '---------------------'

curl -Lo travis_after_all.py https://raw.github.com/jbdeboer/travis_after_all/master/travis_after_all.py
python travis_after_all.py
. .to_export_back

echo BUILD_LEADER=$BUILD_LEADER
echo BUILD_AGGREGATE_STATUS=$BUILD_AGGREGATE_STATUS

if [ "$BUILD_LEADER" = "YES" ]; then
  if [ "$BUILD_AGGREGATE_STATUS" = "others_succeeded" ]; then
    ./scripts/travis/publish-docs.sh
    ./scripts/travis/presubmit.sh
  else
    echo "ERROR: Some Failed, not submitting"
  fi
else
  echo "ERROR: Other builds have not finished, not submitting"
fi
