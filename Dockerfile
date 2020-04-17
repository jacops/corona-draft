FROM python:3.7-slim as base

RUN set -ex && \
    apt-get update && apt-get install -y \
    gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget

RUN set -ex && \
    pip install pyppeteer && \
    pyppeteer-install

FROM python:3.7-slim as builder

WORKDIR /install

COPY setup.py /install/
COPY src /install/src

RUN set -ex && \
    python setup.py bdist_wheel --universal



FROM base

RUN set -ex && \
    pip3 install --no-cache-dir --upgrade pip pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN set -ex && \
    pipenv install --deploy --system

COPY --from=builder /install/dist/ ./dist/
RUN set -ex && \
    pip install --find-links=dist super_draft

WORKDIR /app

COPY entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]

COPY src/worker.py src/start-tournament.py src/generate-token-pickle.py ./
COPY templates ./templates

CMD ["python", "worker.py"]
