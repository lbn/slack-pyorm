import pip

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

links = []
requires = []

requirements = pip.req.parse_requirements(
    "requirements.txt", session=pip.download.PipSession())

for item in requirements:
    # we want to handle package names and also repo urls
    if getattr(item, "url", None):  # older pip has url
        links.append(str(item.url))

    if getattr(item, "link", None):  # newer pip has link
        links.append(str(item.link))

    if item.req:
        requires.append(str(item.req))

config = {
    "description": "PonyORM models for Slack export data",
    "author": "Lee Archer",
    "url": "https://github.com/lbn/slack-pyorm",
    "download_url": "https://github.com/lbn/slack-pyorm",
    "author_email": "lee+github@archer.onl",
    "version": "0.0.1",
    "packages": ["slackpyorm"],
    "scripts": [],
    "name": "slackpyorm",
    "install_requires": requires,
    "dependency_links": links
}

setup(**config)
