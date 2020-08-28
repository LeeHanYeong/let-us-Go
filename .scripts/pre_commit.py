import subprocess
from distutils.spawn import find_executable


class RequiredPackagesNotInstalled(Exception):
    def __init__(self, name, help_text=None):
        self.name = name
        self.help_text = help_text

    def __str__(self):
        return 'Required package "{name}" is not installed.{help}'.format(
            name=self.name, help=f" (try: {self.help_text})" if self.help_text else "",
        )


def run(cmd, **kwargs):
    subprocess.run(cmd, shell=True, **kwargs)


if __name__ == "__main__":
    if not find_executable("poetry"):
        raise RequiredPackagesNotInstalled("poetry", "https://lhy.kr/python-poetry")

    run("poetry export -f requirements.txt > requirements.txt")
    run("poetry export -f requirements.txt --dev > requirements_dev.txt")
    run("git add requirements.txt requirements_dev.txt")
