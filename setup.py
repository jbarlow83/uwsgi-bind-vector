import sys

try:
    from skbuild import setup
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

from setuptools import find_packages

setup(
    name="uwsgi-bind-vector",
    version="0.0.1",
    description="a minimal example package (with pybind11)",
    author="Henry Schreiner",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmake_install_dir="src/uwsgi_bind_vector",
    include_package_data=True,
    extras_require={"test": ["pytest"]},
    python_requires=">=3.6",
    install_requires=[
        "uWSGI==2.0.20",
        "six",
        "Django==4.1.1",
    ],
)
