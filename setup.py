from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='vhdltree',
    version='0.1.0',
    description='Prints the hierarchy of vhdl projects',
    long_description=readme(),
    url='http://github.com/nathdwek/vhdltree',
    author='Nathan Dwek',
    author_email='nathdwek@ulb.ac.be',
    license='MIT',
    packages=['vhdltree'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vhdltree=vhdltree:main'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
    ],
)
