# nebula
It's a simple Ukrainian realty analysis app. Nebula leverages clustering to split
some city's flat set into separate groups according to their placement and price
per square meter.

## Environment
This app implies you've had `conda` installed on your workstation. So just create 
an environment and install the deps:
```bash
$ conda create -n nebula
$ conda activate nebula
$ pip install -r requirements.txt
$ conda deactivate
```

## Usage
To run the app just type: 
```bash
$ conda activate nebula
$ python -m nebula
$ conda deactivate
```
or simply add an alias (according to your `conda` path):
```bash
$ alias nebula="$HOME/anaconda3/envs/nebula/bin/python -m"
$ nebula
```
