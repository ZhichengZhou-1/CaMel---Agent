# CaMeL-phase0 prototype

## Setup

python3 -m venv .venv
source .venv/bin/activate
pip install pydantic networkx rich

## Run demos

# from repo root

python -m runs.demo_benign
python -m runs.demo_attack

# run evaluation harness

python eval/run_suite.py
