import nox

project_name = "pyre"

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True


def deps(session):
    session.install("poetry", "pytest")
    session.run("poetry", "install")


@nox.session()
def black(session):
    deps(session)
    session.install("black")
    session.run("black", ".")


@nox.session()
def tests(session):
    deps(session)
    session.run("pytest", "tests/")


@nox.session()
def coverage(session):
    deps(session)
    session.install("coverage")
    session.run(
        "coverage", "run", f"--source=./{project_name}", "-m", "pytest", "./tests/",
    )
    session.run("coverage", "report", "--fail-under=70", "-m")


@nox.session()
def autopep8(session):
    deps(session)
    session.install("autopep8")
    session.run(
        "autopep8",
        f"{project_name}",
        "--recursive",
        "--aggressive",
        "--aggressive",
        "--aggressive",
        "--in-place",
        "--verbose",
    )


@nox.session()
def flake8(session):
    deps(session)
    session.install("flake8")
    session.run("flake8", f"{project_name}")


@nox.session()
def pylint(session):
    deps(session)
    session.install("pylint")
    session.run("pylint", "--rcfile=./nox.ini", f"./{project_name}")


@nox.session()
def mypy(session):
    deps(session)
    session.install("mypy")
    session.env["MYPYPATH"] = f"./{project_name}"
    session.run("mypy", "--config-file=./nox.ini", f"{project_name}", "tests")


@nox.session()
def build(session):
    deps(session)
    session.run("poetry", "build", "-v")


@nox.session()
def docs(session):
    deps(session)
    session.install("sphinx")
    session.install("sphinx-bootstrap-theme")
    session.run("sphinx-apidoc", "-o", "./docs/source", f"./{project_name}")
    session.run("python", "./docs/make.py", "html")
