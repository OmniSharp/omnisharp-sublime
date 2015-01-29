#!/usr/bin/env bash

function kill_and_be_killed {
	for p in $( ps --ppid $1 --no-headers -o "%p" ) ; do
		kill_and_be_killed $p
	done
	if (( $1 > $$ )) ; then
		kill $1 2>/dev/null
	fi
	return 0
}

$@ &

e=1
while [ $e -gt 0 ] ; do
	sleep 5
	e=`ps -e | grep sublime_text | wc -l`
done

echo "Killing OmniSharp server"

kill_and_be_killed $$