#!/bin/bash
set -Eeuo pipefail

nim c -d:release --app:lib --out:nim_str_utils.so --threads:on nim_str_utils 
pytest -s .
