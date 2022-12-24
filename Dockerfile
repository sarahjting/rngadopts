FROM node:19.3-alpine As npm
WORKDIR /usr/src/app
COPY frontend/ ./
RUN npm install
RUN mode=production npm run build

FROM python:3 as production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY --from=npm /usr/src/app/ ./frontend
