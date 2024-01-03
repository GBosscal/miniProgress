FROM python:3.11.5

ADD . /data

# apt改用清华源
ADD ./sources.list /etc/apt/sources.list

WORKDIR /data

# RUN apt clean && apt autoclean && rm -rf /etc/apt/sources.list.d/*  && apt update -y && apt upgrade -y

# Pip改清华源
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo Asia/Shanghai > /etc/timezone

CMD ["python", "main.py"]