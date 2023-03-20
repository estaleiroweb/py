# Build PyPi Package

## Make sure you have Python and pip installed

```bash
python -V
# Python 3.10.0
python -m pip --version
# pip 23.0.1 from C:\Users\helbe\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)
```
## Install the required packages

```bash
pip install setuptools wheel twine tqdm
```
- setuptools: [Setuptools](https://pypi.org/project/setuptools/) is a package development process library designed for creating and distributing Python packages
- wheel: The [Wheel](https://pypi.org/project/wheel/) package provides a `bdist_wheel` command for `setuptools`. It creates .whl file which is directly installable through the `pip install` command. We'll then upload the same file to [pypi.org](https://pypi.org/)
- twine: The [twine](https://pypi.org/project/twine/) package provides a secure, authenticated, and verified connection between your system and [PyPi](https://pypi.org/) over [HTTPS](https://en.wikipedia.org/wiki/HTTPS)
- tqdm: [Tqdm](https://pypi.org/project/tqdm/) is a smart progress meter used internally by Twine.

## Create your python package.
- Create LICENCE file
  - To see MIT License open [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)
- Create setup.py file
	```python
	import setuptools 

	setuptools.setup( 
		name='<package_name>', 
		version='0.1', 
		author="<author’s name", 
		author_email="<author’s email>", 
		description="<Basic desc>", 
		packages=setuptools.find_packages(), 
		classifiers=[
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		],
	)
	```
- Create requirement.txt with all packages you require in your project

## Test the package
Run every instructions 

## Run setup.py
The command to create whl file
```bash
python setup.py bdist_wheel
```

## Register in PyPi
The Python community maintains a repository similar to npm for open source packages. If you want to make your package publicly accessible you can upload it on PyPi. So, first of all, register yourself on PyPi: [https://pypi.org/account/register/](https://pypi.org/account/register/)

## Upload Package
```bash
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

## Test the package
```bash
pip install <packagename>
```
