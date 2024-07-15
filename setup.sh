#!/bin/bash

CURRENT_DIR=$(pwd)
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt update || exit
sudo apt install -y python3 python3-venv
git clone https://github.com/hyperupcall/autoenv ~/.autoenv

if [[ -f ~/.zshrc ]]; then
    if [[ -z $(grep 'source ~/.autoenv/activate.sh' ~/.zshrc) ]]; then
        echo 'source ~/.autoenv/activate.sh' >> ~/.zshrc
    fi
    if [[ -z $(grep 'export AUTOENV_ENABLE_LEAVE=TRUE' ~/.zshrc) ]]; then
        echo 'export AUTOENV_ENABLE_LEAVE=TRUE' >> ~/.zshrc
    fi
    if [[ -z $(grep 'export VIRTUAL_ENV_DISABLE_PROMPT=' ~/.zshrc) ]]; then
        echo 'export VIRTUAL_ENV_DISABLE_PROMPT=' >> ~/.zshrc
    fi
else
    if [[ -z $(grep 'source ~/.autoenv/activate.sh' ~/.bashrc) ]]; then
        echo 'source ~/.autoenv/activate.sh' >> ~/.bashrc
    fi
    if [[ -z $(grep 'export AUTOENV_ENABLE_LEAVE=TRUE' ~/.bashrc) ]]; then
        echo 'export AUTOENV_ENABLE_LEAVE=TRUE' >> ~/.bashrc
    fi
    if [[ -z $(grep 'export VIRTUAL_ENV_DISABLE_PROMPT=' ~/.bashrc) ]]; then
        echo 'export VIRTUAL_ENV_DISABLE_PROMPT=' >> ~/.bashrc
    fi
fi

cd "$SCRIPT_DIR"

python3 -m venv venv_ip2asn

source venv_ip2asn/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Setup complete"