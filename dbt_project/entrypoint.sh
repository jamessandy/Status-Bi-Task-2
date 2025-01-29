#!/usr/bin/env python3
import os
import subprocess

# Run the Python script
subprocess.run(["python3", "/usr/app/sync_remote_to_local.py"], check=True)

# Run dbt
subprocess.run(["dbt", "run"], check=True)