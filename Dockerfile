FROM comp0174-analyser
RUN apt-get update && apt-get install -y texlive
COPY test.py /comp0174/test.py
