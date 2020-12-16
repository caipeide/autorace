#!/bin/sh

echo "\e[104m Setting up new conda environment \e[0m"
conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch -y
pip install opencv-python
conda install docopt -y
conda install tensorboard -y
conda install matplotlib -y
sed -i '$a\conda activate autorace' ~/.bashrc

echo "\e[104m Install the Donkeycar dependency \e[0m"
cd
mkdir -p ~/projects; cd ~/projects
git clone https://github.com/caipeide/donkeycar.git
cd donkeycar
pip install -e .