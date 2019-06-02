FROM python:3

ARG SCRIPTDIR
ARG RUNNABLE

ENV SCRIPTHOME /opt/structure

ENV SCRIPT ${RUNNABLE}

ADD ./shared_libs ${SCRIPTHOME}/shared_libs
ADD ./${SCRIPTDIR} ${SCRIPTHOME}/${SCRIPTDIR}

RUN pip install -r ${SCRIPTHOME}/${SCRIPTDIR}/PythonDeps/pip_req.txt

WORKDIR ${SCRIPTHOME}/${SCRIPTDIR}

CMD ["sh","-c", "python3 ./${SCRIPT}"]