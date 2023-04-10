FROM python

WORKDIR /java
RUN wget -O - "https://datax-opensource.oss-cn-hangzhou.aliyuncs.com/202303/datax.tar.gz" | tar -xzf - -C /
RUN wget -O - "https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.tar.gz" | tar -xzf - -C ./
ENV JAVA_HOME /java/jdk-20
ENV PATH $JAVA_HOME/bin:$PATH

WORKDIR /data
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80