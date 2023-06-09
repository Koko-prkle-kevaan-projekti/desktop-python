import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "TassuTutka",
    version = "0.0.8",
    author = "Mikko Kujala",
    author_email = "m.kujala@live.com",
    description = ("TassuTutka -project's desktop app."),
    license = "Unlicense",
    url = "https://github.com/Koko-prkle-kevaan-projekti/desktop-python.git",
    packages=['tassu_tutka'],
    entry_points = {
        "console_scripts": [
            "ttutka = tassu_tutka.ttutka:main"
        ]
    },
    install_requires=[
        "anyio == 3.6.2"
        "black == 23.1.0"
        "certifi == 2022.12.7"
        "charset - normalizer == 3.1.0"
        "click == 8.1.3"
        "colorama == 0.4.6"
        "customtkinter == 5.1.2"
        "darkdetect == 0.8.0"
        "decorator == 5.1.1"
        "fastapi == 0.95.0"
        "future == 0.18.3"
        "geocoder == 1.38.1"
        "geojson == 3.0.1"
        "h11 == 0.14.0"
        "httpcore == 0.17.0"
        "httpx == 0.24.0"
        "idna == 3.4"
        "lock == 2018.3.25.2110"
        "mypy - extensions == 1.0.0"
        "packaging == 23.0"
        "pathspec == 0.11.1"
        "Pillow == 9.4.0"
        "platformdirs == 3.1.1"
        "pydantic == 1.10.7"
        "pyperclip == 1.8.2"
        "python - dotenv == 1.0.0"
        "pywin32 == 306"
        "ratelim == 0.1.6"
        "requests == 2.28.2"
        "six == 1.16.0"
        "sniffio == 1.3.0"
        "starlette == 0.26.1"
        "tkintermapview == 1.28"
        "typing_extensions == 4.5.0"
        "urllib3 == 1.26.15"
        "uvicorn == 0.21.1"
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: Unlicense",
    ],
)
