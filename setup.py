from setuptools import setup

PACKAGE_NAME = "viam_minipupper_py"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    packages=[PACKAGE_NAME],
    data_files=[],
    install_requires=["setuptools", "rich", "black", "transforms3d"],
    zip_safe=False,
    maintainer="zmk5",
    maintainer_email="zkakish@gmail.com",
    description="Mini Pupper driver using Viam Python SDK",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "run_pupper_client = viam_minipupper_py.client:main",
            "run_pupper_server = viam_minipupper_py.server:main",
        ],
    },
)
