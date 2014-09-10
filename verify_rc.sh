#!/bin/bash
#
# Usage:
#   ./verify-rc.sh RELEASE_DIRECTORY
#
# It is expected that you have md5deep installed on your system.
# MD5 on OS X 10.9.2 didn't have the ability to verify checksums.
# You can visit the md5deep website for installation instructions
# or use Homebrew if you're on OS X.
#
# http://md5deep.sourceforge.net/
#
# When attempting to import keys for signature verification it is
# assumed that your release is (at the minimum) distributed as a .zip.
# If this is not the case, your key file will not be imported. Adjust
# the extraction code as necessary to accommodate your project's preferred
# distribution format(s).

echo 
echo "------------------"
echo "  Verifying MD5s  "
echo "------------------"
for f in $1/*.md5; do
    echo
    md5deep -M $f ${f%.md5}

    if [ $? -eq 0 ]; then
        echo "MD5 verified"
    else
        echo "MD5 failed to verify"
    fi
done

echo 
echo "------------------------"
echo "  Verifying Signatures  "
echo "------------------------"
unzip $1/*.zip -d ./test >/dev/null 2>&1

if [ -e ./test/KEYS ]; then
    echo "Importing KEYS file from release artifact(s)"
    gpg --import ./test/KEYS
    echo ""
fi

for f in $1/*.asc; do
    echo ""
    gpg --verify $f
    echo ""
done
rm -rf ./test
