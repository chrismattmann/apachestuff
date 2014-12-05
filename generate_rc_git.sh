#!/bin/bash
#
# Usage: ./generate_rc_git.sh PATH_TO_GIT_REPO TAG_NAME ARTIFACT_DIRECTORY [GPG_KEY_NAME]
#
# PATH_TO_GIT_REPO: The path to the git repository that you want to tag a
#   release candidate in.
#
# TAG_NAME: The tag name to use for the release candidate tag.
#
# ARTIFACT_DIRECTORY: Directory into which the release candidate artifacts
#   should be placed.
#
# GPG_KEY_NAME (optional): The key name to use when signing the release artifacts
#   wigh gpg. Check the man pages for the '-u' flag for additional information on
#   how this will be used.

REPO_PATH=$1
TAG_NAME=$2
CUR=`pwd`

cd "$(dirname "$3")"
ARTIFACT_OUT="$(pwd)/$(basename "$3")"
cd $CUR

cd $REPO_PATH
PROJECT=$(git remote -v | grep origin | rev | cut -d '/' -f -1 | rev | cut -d ' ' -f 1 | cut -d '.' -f 1 | uniq)

git tag -a $TAG_NAME -m "Tagging $TAG_NAME"
git push --tags

git archive $TAG_NAME | gzip > "$ARTIFACT_OUT/$PROJECT-$TAG_NAME.tgz"
git archive --format zip --output "$ARTIFACT_OUT/$PROJECT-$TAG_NAME.zip" $TAG_NAME

cd $ARTIFACT_OUT
md5 "$PROJECT-$TAG_NAME.tgz" > "$PROJECT-$TAG_NAME.tgz.md5"
md5 "$PROJECT-$TAG_NAME.zip" > "$PROJECT-$TAG_NAME.zip.md5"

if [ -z $4 ]; then
    gpg --armor --output "$PROJECT-$TAG_NAME.tgz.asc" --detach-sig "$PROJECT-$TAG_NAME.tgz"
    gpg --armor --output "$PROJECT-$TAG_NAME.zip.asc" --detach-sig "$PROJECT-$TAG_NAME.zip"
else
    gpg --armor -u $4 --output "$PROJECT-$TAG_NAME.tgz.asc" --detach-sig "$PROJECT-$TAG_NAME.tgz"
    gpg --armor -u $4 --output "$PROJECT-$TAG_NAME.zip.asc" --detach-sig "$PROJECT-$TAG_NAME.zip"
fi
