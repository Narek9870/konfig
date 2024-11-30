#!/bin/bash
for file in examples/*.cfg; do
    echo "Testing $file"
    python3 config_parser.py < "$file"
done
