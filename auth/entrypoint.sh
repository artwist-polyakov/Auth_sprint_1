#!/bin/bash

uvicorn main:app --proxy-headers --host $AUTH_HOST --port $AUTH_PORT