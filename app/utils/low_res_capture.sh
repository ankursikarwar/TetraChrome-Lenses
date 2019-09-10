#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 256*144 --no-banner ./data/capture/capture.jpg
