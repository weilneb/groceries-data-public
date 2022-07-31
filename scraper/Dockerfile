FROM debian:11-slim
RUN apt-get update
RUN apt-get install -y wget python3-pip unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm ./google-chrome-stable_current_amd64.deb
RUN groupadd -r group1 && useradd --no-log-init -m -r -g group1 user
USER user
WORKDIR /home/user

ARG CHROME_VERSION=106.0.5249.61
RUN wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && rm chromedriver_linux64.zip

RUN mkdir /home/user/vol
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD app app/
COPY ww_products.yml .

CMD ["python3", "-u", "-m", "app"]
#CMD ["/bin/bash"]