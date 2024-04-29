#!/bin/bash

uvicorn main:app --proxy-headers --host $NOTIFICATIONS_HOST --port $NOTIFICATIONS_PORT