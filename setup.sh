#!/bin/bash

python3 -m venv ip2asn_env

source ip2asn_env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete"