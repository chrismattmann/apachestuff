#!/bin/bash
#
# Usage:
#   ./verify-rc.sh RELEASE_DIRECTORY
#

echo 
echo "------------------"
echo "  Verifying MD5s  "
echo "------------------"

./verify_md5_checksums $1

echo 
echo "------------------------"
echo "  Verifying Signatures  "
echo "------------------------"

./verify_gpg_sigs $1

