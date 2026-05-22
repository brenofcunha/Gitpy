import subprocess

def pystatus():
    subprocess.run(["git", "status"])