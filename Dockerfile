FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG IMAGGA_API_KEY
ARG IMAGGA_API_SECRET
ENV IMAGGA_API_KEY=${acc_a8fb70652b8aeb8}
ENV IMAGGA_API_SECRET=${5b8d87121d05a5b67830c1afddb409ff}
ENV FLASK_ENV=production

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]