FROM registry.cn-shenzhen.aliyuncs.com/gindowcloud/python

WORKDIR /data
COPY . .

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80