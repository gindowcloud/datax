FROM registry.cn-shenzhen.aliyuncs.com/gindowcloud/python

WORKDIR /java
RUN wget -O - "https://datax-opensource.oss-cn-hangzhou.aliyuncs.com/202303/datax.tar.gz" | tar -xzf - -C /
RUN wget -O - "https://data.gindow.com/softwares/jdk-8u361-linux-x64.tar.gz" | tar -xzf - -C ./
ENV JAVA_HOME /java/jdk1.8.0_361
ENV PATH $JAVA_HOME/bin:$PATH

WORKDIR /data
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80