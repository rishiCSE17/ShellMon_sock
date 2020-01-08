# installation prerquisits

sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-dev

sudo apt -y install python3 python3-pip figlet
sudo python3.7 -m pip install --upgrade pip

figlet 'ShellMon-Sock by Saptarshi'
echo 'press any key to continue...'
read x
sudo python3 -m pip install numpy matplotlib drawnow psutil
