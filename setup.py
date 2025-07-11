from setuptools import setup, find_packages
import os

# Get the package name from the current directory name
# This script runs in the root of the cloned repo, so os.getcwd() is the repo root
package_name = os.path.basename(os.getcwd()).replace('-', '_')

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
