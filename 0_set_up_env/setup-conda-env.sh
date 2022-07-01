#sh setup-conda-env.sh envname
env_name=$1
conda create -n "${env_name}" python=3.7.11 -y
source activate "${env_name}" 
pip install -r requirements.txt
python -m ipykernel install --user --name "${env_name}" --display-name "${env_name}"