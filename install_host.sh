#!/bin/sh

# https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

set -e

password=$1 # the password used for remote connection to this car.

# Record the time this script starts
date

# Get the full dir name of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Keep updating the existing sudo time stamp
sudo -v
while true; do sudo -n true; sleep 120; kill -0 "$$" || exit; done 2>/dev/null &

# Enable i2c permissions
echo "\e[100m Enable i2c permissions \e[0m"
sudo usermod -aG i2c $USER

# Install pip and some python dependencies
echo "\e[104m Install pip and some python dependencies \e[0m"
sudo apt-get update
sudo apt install -y python3-pip python3-pil python3-smbus python3-matplotlib cmake build-essential python3-dev python3-pandas python3-h5py libhdf5-serial-dev hdf5-tools nano ntp
sudo -H pip3 install --upgrade pip
sudo -H pip3 install flask
sudo -H pip3 install --upgrade numpy

# Install ohmyzsh and zsh-autosuggestions
echo "\e[100m Install ohmyzsh \e[0m"
sudo apt install -y zsh
y | sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
sed -i "71c plugins=(git zsh-autosuggestions)" ~/.zshrc

# Tune the IMX219 camera
# reference: https://www.waveshare.com/wiki/IMX219-160_Camera
echo "\e[100m Tuning the camera \e[0m"
cd
wget https://www.waveshare.com/w/upload/e/eb/Camera_overrides.tar.gz
tar zxvf Camera_overrides.tar.gz 
sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp

# Install jtop
echo "\e[100m Install jtop \e[0m"
sudo -H pip install jetson-stats 

# Install the pre-built PyTorch pip wheel 
echo "\e[45m Install the pre-built PyTorch pip wheel  \e[0m"
cd
wget -N https://nvidia.box.com/shared/static/9eptse6jyly1ggt9axbja2yrmj6pbarc.whl -O torch-1.6.0-cp36-cp36m-linux_aarch64.whl 
sudo apt-get install -y python3-pip libopenblas-base libopenmpi-dev 
sudo -H pip3 install Cython
sudo -H pip3 install numpy torch-1.6.0-cp36-cp36m-linux_aarch64.whl

# Install torchvision package
echo "\e[45m Install torchvision package \e[0m"
cd
git clone https://github.com/pytorch/vision torchvision
cd torchvision
git checkout tags/v0.7.0
sudo -H python3 setup.py install
cd  ../
pip install 'pillow<7'

# Install torch2trt for model acceleration
echo "\e[100m Install torch2trt for model acceleration \e[0m"
cd
git clone https://github.com/NVIDIA-AI-IOT/torch2trt 
cd torch2trt 
sudo python3 setup.py install
cd ../

# Install traitlets (master, to support the unlink() method)
echo "\e[48;5;172m Install traitlets \e[0m"
#sudo -H python3 -m pip install git+https://github.com/ipython/traitlets@master
sudo python3 -m pip install git+https://github.com/ipython/traitlets@dead2b8cdde5913572254cf6dc70b5a6065b86f8

# Install Jupyter Lab
echo "\e[48;5;172m Install Jupyter Lab \e[0m"
sudo apt install -y curl
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt install -y nodejs libffi-dev
sudo -H pip3 install jupyter jupyterlab
sudo -H jupyter labextension install @jupyter-widgets/jupyterlab-manager

jupyter lab --generate-config
python3 -c "from notebook.auth.security import set_password; set_password('$password', '$HOME/.jupyter/jupyter_notebook_config.json')"

# fix for Traitlet permission error
sudo chown -R $USER:$USER ~/.local/share/

# Install jetcard
echo "\e[44m Install jetcard \e[0m"
cd $DIR
pwd
sudo -H python3 setup.py install

# Install jetcard display service
echo "\e[44m Install jetcard display service \e[0m"
python3 -m jetcard.create_display_service
sudo mv jetcard_display.service /etc/systemd/system/jetcard_display.service
sudo systemctl enable jetcard_display
sudo systemctl start jetcard_display

# Install jetcard jupyter service
echo "\e[44m Install jetcard jupyter service \e[0m"
python3 -m jetcard.create_jupyter_service
sudo mv jetcard_jupyter.service /etc/systemd/system/jetcard_jupyter.service
sudo systemctl enable jetcard_jupyter
sudo systemctl start jetcard_jupyter

# Make swapfile
echo "\e[46m Make swapfile \e[0m"
cd
if [ ! -f /var/swapfile ]; then
	sudo fallocate -l 4G /var/swapfile
	sudo chmod 600 /var/swapfile
	sudo mkswap /var/swapfile
	sudo swapon /var/swapfile
	sudo bash -c 'echo "/var/swapfile swap swap defaults 0 0" >> /etc/fstab'
else
	echo "Swapfile already exists"
fi

# Install remaining dependencies for projects
echo "\e[104m Install remaining dependencies for projects \e[0m"
sudo apt-get install python-setuptools

# Install DonkeyCar
# reference: http://docs.donkeycar.com/guide/robot_sbc/setup_jetson_nano/
echo "\e[104m Setting up python virtual environment \e[0m"
pip3 install virtualenv
python3 -m virtualenv -p python3 env --system-site-packages
echo "source ~/env/bin/activate" >> ~/.bashrc
echo "source ~/env/bin/activate" >> ~/.zshrc
cd $DIR
gnome-terminal -- bash -c "sh ./donkeycar.sh; exec bash;"

echo "\e[42m Install the donkeycar depencency in a new terminal... \e[0m"
#record the time this script ends
date

