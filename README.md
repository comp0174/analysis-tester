# COMP0174 Grader

Build a grader image (requires `comp0174-analyser` image):

    docker build . -t comp0174-grader

To grade a submission, run the following command:

    docker run -ti --rm \
        -v <path to submission>:/comp0174/submission \
        -v <path to tests>:/comp0174/tests \
        comp0174-grader \
        python3 grade.py tests submission
    
