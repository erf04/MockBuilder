from setuptools import setup, find_packages

setup(
    name="mocksql",  # Package name
    version="0.1.0",    # Initial version
    author="erfan kazemzadeh",
    author_email="erfank20041382@gmail.com",
    description="A mock data builder for sql databases",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/erf04/MockBuilder",  # Project URL
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[
        "Faker>=33.1.0",
        "PyYAML>=6.0.2"  # Example dependency
    ],
)
