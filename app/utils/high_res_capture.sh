#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 640*480 --no-banner ./data/capture/capture.jpg
