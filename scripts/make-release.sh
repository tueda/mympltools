#!/bin/bash
#
# Make a release tag.
#
# Usage:
#   make-release
#   make-release NEW-VERSION
#   make-release NEW-VERSION NEW-DEV-VERSION

set -eu
set -o pipefail

###

# Project-specific code

# Tag prefix.
v=''

# pre_version_message <current_version_number> <version_number> <dev_version_number>:
# a hook function to print some message before bumping the version number.
function pre_version_message() {
  echo 'Please make sure that CHANGELOG is up-to-date.'
  echo 'You can use the output of the following command:'
  echo
  echo "  git-chglog --next-tag $v$2"
  echo
}

# version_bump <version_number>: a hook function to bump the version for documents.
function version_bump() {
  dev_version_bump $1
  local urlbase=git+https://github.com/tueda/mympltools.git
  sed -i "s|pip install $urlbase@.*|pip install $urlbase@$v$1|" README.md
  sed -i "s|poetry add $urlbase@.*|poetry add $urlbase@$v$1|" README.md
  sed -i "s|Install mympltools .* only when running on|Install mympltools $1 only when running on|" examples/Examples.ipynb
  sed -i "s|pip install $urlbase@.*\"|pip install $urlbase@$v$1\"|" examples/Examples.ipynb
  # Check if the files are changed.
  [[ $(numstat README.md) == '2,2' ]]
  [[ $(numstat examples/Examples.ipynb) == '2,2' ]]
}

# dev_version_bump <dev_version_number>: a hook function to bump the version for code.
function dev_version_bump() {
  :
}

###

# abort <message>: aborts the program with the given message.
function abort {
  echo "error: $@" 1>&2
  exit 1
}

# isclean: checks if the working repository is clean (untracked files are ignored).
function isclean() {
  [[ $(git diff --stat) == '' ]] && [[ $(git diff --stat HEAD) == '' ]]
}

# numstat <file>: prints number of added and deleted lines for the file (e.g., "0,0").
function numstat() {
  local stat
  stat=$(git diff --numstat "$1")
  if [[ $stat =~ ([0-9]+)[[:blank:]]+([0-9]+) ]]; then
    echo "${BASH_REMATCH[1]},${BASH_REMATCH[2]}"
  else
    echo 0,0
  fi
}

# First, trap ERR to print the stack trace when a command fails.
# See: https://gist.github.com/ahendrix/7030300
function _errexit() {
  local err=$?
  set +o xtrace
  local code="${1:-1}"
  echo "Error in ${BASH_SOURCE[1]}:${BASH_LINENO[0]}: '${BASH_COMMAND}' exited with status $err" >&2
  # Print out the stack trace described by $FUNCNAME
  if [ ${#FUNCNAME[@]} -gt 2 ]; then
    echo "Traceback:" >&2
    for ((i=1;i<${#FUNCNAME[@]}-1;i++)); do
      echo "  [$i]: at ${BASH_SOURCE[$i+1]}:${BASH_LINENO[$i]} in function ${FUNCNAME[$i]}" >&2
    done
  fi
  echo "Exiting with status ${code}" >&2
  exit "${code}"
}
trap '_errexit' ERR
set -o errtrace

# Abort if the working directory is dirty.
isclean || abort 'working directory is dirty'

# Ensure that we are in the project root.
cd $(git rev-parse --show-toplevel)

# Determine the current and next versions.
# The current version is determined with Poetry.
# The default next_version is determined with Git as CalVer (YY.MM.MICRO),
# see https://calver.org/.
current_version=$(poetry version -s)
patch_version=0
while :; do
  next_version=$(date '+%-y.%-m').$patch_version
  if [[ -z $(git tag -l "$v$next_version") ]]; then
    break
  fi
  ((patch_version++)) || :
done
next_dev_version=prepatch
if [[ $# -ge 2 ]]; then
  next_version=$1
  next_dev_version=$2
elif [[ $# -eq 1 ]]; then
  next_version=$1
fi
poetry version $next_version >/dev/null
next_version=$(poetry version -s)
poetry version $next_dev_version >/dev/null
next_dev_version=$(poetry version -s)
git restore pyproject.toml

# Print the versions and confirm if they are fine.
pre_version_message $current_version $next_version $next_dev_version
echo 'This script will bump the version number.'
echo "  current commit      : $(git rev-parse --short HEAD)"
echo "  current version     : $current_version"
echo "  next version        : $next_version"
echo "  next dev-version    : $next_dev_version"
while :; do
  read -p 'ok? (y/N): ' yn
  case "$yn" in
    [yY]*)
      break
      ;;
    [nN]*)
      echo 'Aborted' >&2
      exit 1
      ;;
    *)
      ;;
  esac
done

# Bump the version with Poetry and Git.
poetry version $next_version
version_bump $next_version
git commit -a -m "chore(release): bump version to $next_version"
git tag $v$next_version
poetry version $next_dev_version
dev_version_bump $next_dev_version
git commit -a -m "chore: bump version to $next_dev_version"

# Completed. Show some information.
echo "A release tag $v$next_version was successfully created."
echo "The current development version is now $next_dev_version"
echo "To push it to the origin:"
echo "  git push origin $v$next_version"
