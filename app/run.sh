#!/bin/bash
gunicorn -w 1 -b 0.0.0.0:30027 run_app:app
