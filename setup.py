from setuptools import setup, find_packages
import re

# auto-updating version code stolen from orbitize! stolen from RadVel
def get_property(prop, project):
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open(project + "/__init__.py").read(),
    )
    return result.group(1)

def get_requires():
    reqs = []
    for line in open("requirements.txt", "r").readlines():
        reqs.append(line)
    return reqs

setup(
    name="astroQTpy",
    version=get_property("__version__", "astroqtpy"),
    description="astroQTpy implements a quadtree data structure to explore 2D parameter space",
    url="https://github.com/CalebHarada/astroQTpy",
    author="Caleb K. Harada",
    author_email="charad@berkeley.edu",
    license="MIT",
    packages=find_packages(),
    keywords="Quadtree Astronomy",
    install_requires=get_requires(),
)