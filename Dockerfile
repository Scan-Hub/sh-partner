FROM 420811272222.dkr.ecr.ap-southeast-1.amazonaws.com/esollabs/cicd:sh-python-0ae89c5-dirty


COPY requirements.txt /
COPY lib/requirements.txt /lib/requirements.txt
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r /lib/requirements.txt
RUN pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install "Flask[async]"

COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps
WORKDIR /webapps