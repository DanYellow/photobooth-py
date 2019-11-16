FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip3 install python-dotenv
RUN pip3 install qrcode

RUN pip3 uninstall PIL
RUN pip3 uninstall Pillow
RUN pip3 install Pillow

# RUN pip install -r requirements.txt
# RUN pip install pipenv


# RUN pipenv install --dev 
# \ && pipenv lock -r > requirements.txt

ENV DISPLAY :0

CMD python main.py