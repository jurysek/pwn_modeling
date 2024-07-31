# pwn_modeling
Code for modeling of Pulsar Wind Nebula development in time-dependent environment. As the time-dependent environment, an approximate model of PWN expanding inside SNR implemented in gammapy (https://github.com/gammapy) is used. The particle distributions and particle radiation is calculated in this changing environment with the use of the Gamera package (https://github.com/libgamera/GAMERA). Caveats: Impact of the radiation energy loss on the PWN expansion is not taken into account. PWN radius is assumed constant after the interaction with the reverse shock.

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
