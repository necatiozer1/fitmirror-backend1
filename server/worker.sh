#!/usr/bin/env bash
celery -A app.cel worker --loglevel=INFO
