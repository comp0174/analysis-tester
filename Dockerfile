FROM comp0174-analyser
RUN apt-get update && apt-get install -y texlive
COPY grade.py /comp0174/grade.py
