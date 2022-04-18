FROM python:3.10-slim

# Configure environments vars. Overriden by GitHub Actions
ENV INPUT_SNOWFLAKE_ACCOUNT=
ENV INPUT_SNOWFLAKE_USERNAME=
ENV INPUT_SNOWFLAKE_PASSWORD=
ENV INPUT_SNOWFLAKE_WAREHOUSE=
ENV INPUT_QUERY_FILE=

# setup python environ
RUN apt update && apt upgrade -y
RUN apt install -y libssl-dev libffi-dev build-essential
RUN pip install --user pdm && pdm install

COPY . .

# command to run in container start
CMD ["$HOME/.local/bin/pdm", "run", "python", "${APP_DIR}/main.py"]
