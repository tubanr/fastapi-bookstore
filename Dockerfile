# 
FROM python:3.9

# 
WORKDIR /code/app

# 
COPY ./requirements.txt /code/app/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

# 
COPY ./ /code/app

EXPOSE 8000

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
