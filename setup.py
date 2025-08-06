from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='azampay-sdk-anga',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests', 'python-dotenv'
    ],
    description='A dynamic Python SDK for AzamPay (AzamPay Python SDK used for native python, Django, Flask, FastApi e.t.c)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anganile Adam (Anga)',
    author_email='twaloadam@gmail.com',
    url='https://github.com/tbwahacker/azampay-sdk-anga',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
