FROM python:3.10-slim

# Configure environments vars. Overriden by GitHub Actions
ENV INPUT_SNOWFLAKE_ACCOUNT=
ENV INPUT_SNOWFLAKE_USERNAME=
ENV INPUT_SNOWFLAKE_PASSWORD=
ENV INPUT_SNOWFLAKE_WAREHOUSE=
ENV INPUT_QUERY_FILE=
ENV APP_DIR=/app

WORKDIR ${APP_DIR}

# setup python environ
COPY . ${APP_DIR}
RUN pip install --user pdm && pdm install

# command to run in container start
CMD pdm run python ${APP_DIR}/main.py
