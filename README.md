# COMP0174 Tester

Build a tester image (requires `comp0174-analyser` image):

    docker build . -t comp0174-tester

To test the example analyses on the example tests, run the following command:

    docker run -ti --rm \
        -v <path to example-analyses>:/comp0174/analyses \
        -v <path to example-tests>:/comp0174/tests \
        -v <path to output dir>:/comp0174/output \
        comp0174-grader \
        python3 grade.py tests analyses --report output/report.pdf
        
Then, you can open the generated `report.pdf` for detailed information.
    
