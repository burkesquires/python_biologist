#! /bin/bash
#> SYNOPSIS
#>     ./build.sh deffile imagename
set -e

function die {
    echo "$@" >&2
    exit 1
}

def_file=${1:-none}
[[ "$def_file" != "none" ]] || die "USAGE: build.sh deffile imagename"
image_name=${2:-none}
[[ "$image_name" != "none" ]] || die "USAGE: build.sh deffile imagename"
# final name of the image; also directory name for bootstrap
image=${PWD}/${image_name}
# temp name for the image file when first created
tmp=${image}.tmp
[[ -e "$tmp" || -e "$image" ]] && die "Image file or temp dir already exists"

mkdir $image
sudo chown root:root $image

sudo singularity bootstrap $image $def_file
size_mb=$(sudo du -ms $image | awk '{print $1 + 200}')
sudo singularity create -s $size_mb $tmp
pushd $image
sudo tar -c ./* | sudo singularity import $tmp
popd 

# delete the temp dir
sudo rm -rf $image
# rename the image file to its final name
mv $tmp $image
