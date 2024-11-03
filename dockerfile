FROM python:3.13.0
WORKDIR /Climax
COPY . /Climax/
EXPOSE 5000
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "Climax.py"]