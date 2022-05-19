import pipfile
from setuptools import find_packages, setup


def find_required(section: str = "default"):
    pf = pipfile.load()
    return [f"{key}{val}" for key, val in pf.data[section].items()]


setup(
    name="vedro-jj",
    version="0.0.1",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Tsvetkov",
    author_email="nikitanovosibirsk@yandex.com",
    python_requires=">=3.8",
    url="https://github.com/nikitanovosibirsk/vedro-jj",
    license="Apache-2.0",
    packages=find_packages(exclude=("tests",)),
    package_data={"vedro_jj": ["py.typed"]},
    install_requires=find_required(),
    tests_require=find_required("develop"),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
)
