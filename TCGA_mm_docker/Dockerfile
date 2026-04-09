FROM python:3.9-slim
COPY ./TCGA_matchmaker_project-0.1.0.tar.gz /tmp/ 

RUN pip install numpy
RUN pip install pandas
RUN pip install /tmp/TCGA_matchmaker_project-0.1.0.tar.gz

RUN rm -f /tmp/TCGA_matchmaker_project-0.1.0.tar.gz

WORKDIR /usr/local/src/TCGAmm

COPY ./runTCGAmm_example.py ./

CMD python runTCGAmm_example.py


