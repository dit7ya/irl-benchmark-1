# irl-benchmark



# RL module

For our reinforcement learning module (used to train (near) optimal agents for expert demonstrations and as crucial part of the IRL algorithms), we make use of [SLM lab](https://github.com/kengz/SLM-Lab), a modular deep reinforcement learning framework based on PyTorch. Documentation can be found [here](https://kengz.gitbooks.io/slm-lab/content/).

We currently use a fork of this framework, at some point we might make a pull request and use the original repository. To install please do the following steps:

### Code review, git and github

We use pull requests and code reviews.

Recommended workflow:

1. Make sure your local master branch is up to date with remote master. (`git pull --rebase`)
2. Work directly on master
3. When you are done, commit your changes
4. Push your changes to remote branchname (`git push origin HEAD:branchname`)
5. Open a pull request on github
6. Make changes to your files based on reviews. Push these changes to the same branch, (`git push origin HEAD:branchname`)
7. When everything is working, "Squash and merge" your pull request on Github and celebrate the merge!
8. Click "Delete branch" on github to keep it clean (can be restored later)

Before you push, automagically run all tests with the command: 

`pytest`

For your local work you can also choose to checkout a new branch to work on in step 2. (`git checkout -b branchname`)


## Installation
Install package (from root folder):

`pip install -e .`

### Installing with Yarn (official)

```shell
git clone https://github.com/JohannesHeidecke/SLM-Lab.git
cd SLM-Lab
```

```shell
brew install node yarn
yarn install
```

```shell
conda env update -f environment.yml
pip install -e .
```

### Alternative installation

Tested for Ubuntu 16.04, should mostly work everywhere.

First, you need Python 3.6. Many distros have this by default, Ubuntu 16.04 only
has until 3.5.
```sh
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6 python3.6-dev python3.6-venv
```

We also need other dependencies:
```sh
sudo apt-get install libopencv-dev python3-h5py python-opencv cmake swig
```

Then, you can install the Python packages. I recommend creating a virtual env with python 3.6 and running that in there:
```sh
python3.6 -m venv /desired/path/to/venv
. /desired/path/to/venv/bin/activate

pip install -r slm_requirements.txt
pip install -e /path/to/cloned/SLM-lab
```


There is also a Javascript app, `orca` that is used to look at plots. At some
point you will have to install it like this:
```sh
sudo npm install -g electron@1.8.4 orca
```
