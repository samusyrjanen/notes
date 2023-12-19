# Preparation
1. Clone the repository (`git clone https://version.helsinki.fi/luoyumo/engineering_of_ml_systems.git`). You will be asked to enter a username and password, these are your university credentials. 
1. Install Anaconda from [its offcicial website](https://docs.anaconda.com/free/anaconda/install/index.html).
1. Set up your conda env. 
```bash
# Create a new conda env and activate it 
# Note: KServe client SDK (one of the Python packages for communicating with the MLOps platform) has some conflicts with python 3.11 so we fix the version to 3.10
conda create -n mlops_eng -yf python==3.10 ipykernel
conda activate mlops_eng
```
Remember to ensure that you are always in the correct Python environment.

4. Install [Ansible](https://docs.ansible.com/ansible/latest/index.html), which is a tool for running commands/scripts in remote machines from your local machine. 
```bash
python3 -m pip install --user ansible
```
5. Install [kubectl (version 1.24.0)](https://kubernetes.io/docs/tasks/tools/#kubectl), which is the tool used to communicate with the K8s cluster.

6. Create a `.kube` directory if it does not exist. This directory will be used to save a configuration file of your K8s cluster that will be created later.
```bash
mkdir ~/.kube
```

After finishing the preparation, continue with the "2. Create a VM in cPouta" section in the [main instructions](../README.md#2-create-a-vm-in-cpouta). 