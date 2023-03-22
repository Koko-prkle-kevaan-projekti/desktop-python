import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "TassuTutka",
    version = "0.0.7",
    author = "Mikko Kujala",
    author_email = "m.kujala@live.com",
    description = ("TassuTutka -project's desktop app."),
    license = "Unlicense",
    url = "https://github.com/Koko-prkle-kevaan-projekti/desktop-python.git",
    packages=['tassu_tutka']
    entry_points = {
        "console_scripts": [
            "ttutka = tassu_tutka.ttutka:main"
        ]
    },
    install_requires=[
        "black==23.1.0",
        "certifi==2022.12.7",
        "charset-normalizer==3.1.0",
        "click==8.1.3",
        "customtkinter==5.1.2",
        "darkdetect==0.8.0",
        "decorator==5.1.1",
        "future==0.18.3",
        "geocoder==1.38.1",
        "geojson==3.0.1",
        "idna==3.4",
        "mypy-extensions==1.0.0",
        "packaging==23.0",
        "pathspec==0.11.1",
        "Pillow==9.4.0",
        "platformdirs==3.1.1",
        "pyperclip==1.8.2",
        "ratelim==0.1.6",
        "requests==2.28.2",
        "six==1.16.0",
        "tkintermapview==1.28",
        "urllib3==1.26.15",
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Unlicense",
    ],
)

