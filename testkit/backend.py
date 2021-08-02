"""
Executed in driver container running the image that ./Dockerfile produces.
This script is responsible for starting TestKit backend.
"""
import subprocess

if __name__ == "__main__":
    with open("/artifacts/backenderr.log", "w") as err, \
         open("/artifacts/backendout.log", "w") as out:
        subprocess.check_call(
            ["python", "-m", "testkitbackend"], stdout=out, stderr=err
        )
