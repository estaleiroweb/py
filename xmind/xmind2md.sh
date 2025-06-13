#!/bin/env bash

# ./xmind_markdown_converter/xmind2md.sh '/d/Docs/Particular/My Maps/MP XMind' '/d/Docs/Particular/My Maps/MD'

THIS_DIR=$(dirname "$0")
FROM_DIR="$1"
TO_DIR="$2"
FROM_DIR="${FROM_DIR%/}"
TO_DIR="${TO_DIR%/}"

function check_args() {
	if [ ! "$FROM_DIR" ] || [ ! "$TO_DIR" ]; then
		echo "$0 <path_from> <path_to>"
		exit
	fi

	if [ ! -d "$FROM_DIR" ]; then
		echo "Path $FROM_DIR not exists"
		exit
	fi
}
function exec() {
	[ -d "$1" ] && return
	local FILE=$(basename "$1")
	local EXTENSION="${FILE##*.}"
	local RELATIVE_PATH="${1#$FROM_DIR/}"
	local TO_PATH=$(dirname "$TO_DIR/$RELATIVE_PATH")

	mkdir -p "$TO_PATH"
	if [ "$EXTENSION" = "xmind" ]; then
		FILE="${FILE%.*}.md"
		"$THIS_DIR/xmind_md.py" "$1" "$TO_PATH/$FILE"
	else
		cp -p "$1" "$TO_PATH/"
	fi
}

check_args
IFS=$'\n' && for i in $(find "$1"); do
	exec $i
done
