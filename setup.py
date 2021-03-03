import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="glenn_has_range",  # Replace with your own username
    version="0.0.1",
    author="Robbie Hughes",
    author_email="rwhughes91@gmail.com",
    description="A small API for spotify playlists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rwhughes91/glenn_has_range",
    project_urls={
        "Bug Tracker": "https://github.com/rwhughes91/glenn_has_range/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
