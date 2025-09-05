#!/bin/bash
MODEL_NAME="$1"
shift

hf download "$MODEL_NAME" --local-dir "./models/$MODEL_NAME"