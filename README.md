# pwn_modeling
Code for modeling of Pulsar Wind Nebula development in time-dependent environment. This code is based on Gamera package (https://github.com/libgamera/GAMERA)

## Installation
- install GAMERA, following instructions on https://libgamera.github.io/GAMERA/docs/download_installation.html
- instal PWN modeling package following instructions below
```
PWN_VER=0.1.0

git clone git@github.com:jurysek/pwn_modeling.git
cd pwn_modeling
conda env create -n pwn-modeling-$PWN_VER -f environment.yml
conda activate pwn-modeling-$PWN_VER
pip install -e .
```
