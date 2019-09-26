#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 注意: 要使用此文件的“上传”功能，必须要安装 twine:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# 打包元数据
NAME = "mypackage"
DESCRIPTION = "My short description for my project."
URL = "https://github.com/me/myproject"
EMAIL = "me@example.com"
AUTHOR = "Awesome Soul"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.1.0"

# 该模块依赖了哪些包？
REQUIRED = [
    # 'requests', 'maya', 'records',
]

# 哪些包是可选的？
EXTRAS = {
    # 'fancy feature': ['django'],
}


# 其他的你就不需要改太多了:)
# ------------------------------------------------
# 除了 License 和 Trove Classifiers!
# 如果你要更改 License, 请记得也要改 Trove Classifier!

here = os.path.abspath(os.path.dirname(__file__))

# 导入 README 并将其用作长描述。
# 注意：只有你的 MANIFEST.in 文件中存在'README.md'时才会起作用！
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# 加载包中的 __version__.py 模块
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """支持 setup.py 上传"""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """用粗体打印"""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# 奇迹发生的地方:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # 如果你的 package 是单个模块，请使用此代替“packages”：
    # py_modules=['mypackage'],
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
