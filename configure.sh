sudo apt update
sudo apt upgrade

sudo apt install python3.8
apt-get install python3-pip

git clone https://github.com/Winfredy/SadTalker
cd SadTalker
export PYTHONPATH=/home/ubuntu/SadTalker:$PYTHONPATH

python3.8 -m pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
sudo apt update
sudo apt install ffmpeg
python3.8 -m pip install -r requirements.txt

rm -rf checkpoints
bash scripts/download_models.sh
