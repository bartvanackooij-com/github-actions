# Container image that runs your code
FROM python:3.8-slim

# renovate: datasource=github-releases depName=hashicorp/terraform
# todo: tflint
ENV TERRAFORM_VERSION=1.6.1
ENV INFRACOST_VERSION=v0.10.29

RUN apt update && \
  apt install --no-install-recommends -y \
      unzip \
      git \
      wget

COPY requirements.txt .
RUN pip install -r requirements.txt

# install local packages
COPY /src/ /tmp/src
COPY setup.py /tmp
RUN pip install /tmp/ \
    && rm -rf /tmp/src

COPY /entrypoints/ /entrypoints/
COPY /src/ /src/ 

# install terraform
RUN cd /tmp && \
    wget --tries=3 https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/terraform && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# install infracost (tf cost estimation)
RUN cd /tmp && \
    wget --tries=3 https://github.com/infracost/infracost/releases/download/${INFRACOST_VERSION}/infracost-linux-amd64.tar.gz &&\
    tar -zxvf infracost-linux-amd64.tar.gz && \
    mv infracost-linux-amd64 /usr/local/bin/infracost && \
    rm infracost-linux-amd64.tar.gz