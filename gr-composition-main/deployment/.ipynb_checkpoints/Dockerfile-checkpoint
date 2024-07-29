FROM python:3.8

RUN mkdir /opt/ml /opt/ml/input /opt/ml/input/config /opt/ml/input/data /opt/ml/input/data/training /opt/ml/model /opt/ml/output /opt/program

# Set a docker label to enable container to use SAGEMAKER_BIND_TO_PORT environment variable if present
# LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask gevent gunicorn && \
        rm -rf /root/.cache

WORKDIR /opt/program
ADD deployment/requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=/opt/program
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

COPY deployment/code/nginx.conf /opt/program/
COPY deployment/code/predictor.py /opt/program/
COPY deployment/code/serve /opt/program/
COPY deployment/code/wsgi.py /opt/program/
COPY deployment/code/utils/* /opt/program/utils/
COPY deployment/model/model.pkl /opt/ml/model/
COPY deployment/model/current_model.tar.gz /opt/ml/model/
COPY deployment/model/model.tar.gz /opt/ml/model/
COPY deployment/contract/contrato_dados.json /opt/program/deployment/contract/
COPY tests/ /opt/program/tests/
COPY pytest.ini /opt/program/


# copy pytest.ini /opt/program/
# copy tests/* opt/program/tests/
# copy deployment/contract/contrato_dados.json /opt/program/

RUN chmod +x /opt/program/serve

WORKDIR /opt/program
