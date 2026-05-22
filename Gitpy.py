import typer
from Gitservice import py_status
from Gitservice import py_commit
from Gitservice import py_branch

app = typer.Typer()

@app.command()
def status():
    py_status.pystatus()

@app.command()
def branch():
    py_branch.pybranch()

@app.command()
def commit():
    py_commit.pycommit()    


if __name__ == "__main__":
    app()    