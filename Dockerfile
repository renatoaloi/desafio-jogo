FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV JOGO_RESULTADO_URL="http://**ip_do_seu_pc**:5000/jogo/resultado"

COPY . .

CMD [ "python", "./app.py" ]