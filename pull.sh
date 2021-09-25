#!/bin/bash

# Bash script for recursively pulling git repositories
# Help: bash pull.sh --help
# Aki Hakune, September 21st 2021



# Parse arguments (src: https://stackoverflow.com/a/29754866)
set -o errexit -o pipefail -o noclobber -o nounset
! getopt --test > /dev/null 
if [[ ${PIPESTATUS[0]} -ne 4 ]]; then
    echo "I’m sorry, $(getopt --test) failed in this environment."
    exit 1
fi
OPTIONS=ihd:e:
LONGOPTS=interactive,help,directory:,exclude:
! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTS --name "$0" -- "$@")
if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
    exit 2
fi
eval set -- "$PARSED"
interactive="n" help_text="n" directory=. exclude=-

while true; do
    case "$1" in
        -i|--interactive) interactive="y"; shift ;;
        -d|--directory) directory="$2"; shift 2 ;;
        -e|--exclude) exclude="$2"; shift 2 ;;
        -h|--help) help_text="y"; shift ;;
        --) 
            shift
            break
            ;;
        *)
            echo "Encountered programming error."
            exit 3
            ;;
    esac
done



print_help() {
    echo "usage: bash pull.sh

optional arguments:
-i, --interactive Start interactive mode
-d, --directory   Top directory to pull
-e, --exclude     Excluding repository (case-sensitive)
"
}



# main function, for consistency with C++ structure
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ "$help_text" == "y" ]; then
        print_help "$@"
    fi

    # Note: -i option is not supported on OSX 10.7
    if [ "$interactive" == "y" ]; then
        echo "Interactive mode enabled."
        read -e -p "Root directory(ies) for execution: " -i . directory
        read -e -p "Repostories to exclude from this script: " exclude
    fi

    if [ "$interactive" != "y" ]; then
        echo "Executing with following arguments: 
Executing directory: $directory
Excluding repo: $exclude"
        read -n 1 -s -r -p "Press any key to continue..."
        echo
    fi

    # actual pulling

    # cannot use 'mapfile' due to its not cross-bashes attribute
    git_dirs=()
    while IFS= read -r line; do
        git_dirs+=( "${line%"/.git"}" )
    done < <( find $directory -type d -name ".git")


    for d in ${git_dirs[@]}; do
        if [ "${d##*/}" != "$exclude" ]; then
            dir=$d
            echo "Working on $dir"
            git -C $dir pull
        fi
    done

fi