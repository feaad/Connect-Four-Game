FROM python:3.11-alpine3.17
LABEL maintainer="feaad"

# Prevent Python from writing pyc files to files
ENV PYTHONDONTWRITEBYTECODE 1

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

ENV PATH="/scripts:${PATH}"

# Copy the application code
COPY ./app /app

# Set the working directory
WORKDIR /app

# Copy pyproject.toml files
COPY pyproject.toml /app/

# Copy the scripts to the container
COPY ./scripts /scripts

# Expose the port
EXPOSE 8000

ARG DEV=False

RUN apk add --update --no-cache postgresql-client && \
	apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers\
	build-base python3-dev postgresql-dev musl-dev libpq-dev && \
	pip install --upgrade pip && \
	pip install poetry && \
	poetry config virtualenvs.create false && \
	if [ $DEV = "True" ]; then \
	poetry install --with dev; \
	else \
	poetry install --no-dev; \
	fi && \
	apk del .tmp-build-deps && \
	rm -rf /root/.cache

#  Make all the scripts executable
RUN	chmod +x /scripts/*

# Create a volume for the application
RUN mkdir -p /vol/web/media && \
	mkdir -p /vol/web/static

# Create a user to run the application
RUN	adduser -D cfu

# Change the ownership of the volume
RUN chown -R cfu:cfu /vol && \
	chmod -R 755 /vol/web

# Change the user to cfu
USER cfu

# Set environment path
ENV PATH="/scripts:/venv/bin:$PATH"

# Define the command to run the application
CMD ["entrypoint.sh"]