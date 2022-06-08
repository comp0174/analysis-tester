#!/bin/bash

# Change names such as Participant_4006831_assignsubmission_file_ to 4006831
function rename_moodle_directories {
    for d in $(ls); do mv $d $(echo $d | cut -c 13-19); done
}

function extract_analysis_scripts {
    for d in $(ls); do
        zip="$d/*.zip"
        rm -rf tmp/*
        mkdir -p tmp
        unzip "$zip" -d tmp &>/dev/null
        find tmp -name '*.dl' -not -path '*/.*' -exec mv '{}' "$d" \;
    done
    rm -rf tmp
}

function grade_submission {
    docker run -ti --rm -v $PWD/submissions/$1:/comp0174/submission -v $PWD/../comp0174-analysis-hidden-tests:/comp0174/tests comp0174-grader python3 grade.py tests submission
}
