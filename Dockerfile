FROM python:3.10-slim

# Configure environments vars. Overriden by GitHub Actions
ENV INPUT_SNOWFLAKE_ACCOUNT=
ENV INPUT_SNOWFLAKE_USERNAME=
ENV INPUT_SNOWFLAKE_PASSWORD=
ENV INPUT_SNOWFLAKE_WAREHOUSE=
ENV INPUT_QUERY_FILE=
ENV APP_DIR=/app

WORKDIR $APP_DIR

RUN apt update -y
RUN apt install -y libssl-dev libffi-dev build-essential

# setup python environ
# ENV PATH="$PATH:/root/.local/bin"
# for some reason python in docker is not looking for packages in all places specified in PATH
# therefore manually install the packages to where it looks for them
RUN python -m pip install --target=/usr/local/lib/python3.10/site-packages/ snowflake-connector-python==2.7.6 python-dotenv

COPY . ./

# command to run in container start
CMD python ${APP_DIR}/main.py
