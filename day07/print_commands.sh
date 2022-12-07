#!/bin/bash

# would be fun to use this ;)
# ... unfortunately in a real file system directories also have a size
cat input.txt | grep -v "\$ ls" | sed 's%\([0-9]\+\) \(.*\)%dd if=/dev/zero of=\2 bs=\1 count=1%g' | sed 's/\$ //g' | sed 's/dir/mkdir/' | sed 's%cd /%mkdir folder;cd folder%'
