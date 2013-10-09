#! /bin/sh
# @author: Philippe Coval <mailto:philippe.coval@eurogiciel.com>
# @description: manage git submodules with git-build-package-rpm

set -x
set -e

cat .gitmodules || return 1


git submodule status | awk '{ print $2 }' | while read dir  ; do
    name=$(basename "$dir" )
    echo "name="
    echo "dir=$dir"
    git submodule init
    git submodule update

    tar cjvf "./packaging/${name}.tar.bz2" "${dir}"

    cat<<EOF
# Please add "SourceN: $name.tar.bz2" and "%setup -q -T -D -a N" to "packaging/*.spec"
EOF

done

