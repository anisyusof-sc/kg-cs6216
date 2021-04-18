# Preemptive Anomaly Detection of IoT Network on Knowledge Graph

## Source File Location
- GitHub code repository - [link](https://github.com/anisyusof-sc/kg-cs6216)
- code & binary files - [link](https://mynbox.nus.edu.sg/a/OQjG8_AIxtcrCMbS/afc67eea-269e-4f86-9ba9-552cfbdd264c?l)

## Using Ampligraph
### for non-temporal models
1) Follow the instruction [here](https://github.com/Accenture/AmpliGraph) to install Ampligraph
2) Run one of the model code in /ampligraph/ampligraph_*.py

Example:
```console
$: conda activate ampligraph
$: python3 ampligraph_TransE.py
```

## Using Horovod
### for both TA-based & DE-based models
1) Follow the instructions [here](https://github.com/horovod/horovod#install) to install Horovod
2) Follow the instructions [here](https://github.com/kahrabian/tkgc) to install the TKGC codes
3) Run one of the TKGC models

Example:
```console
$: horovodrun -np 2 -H localhost:2 python -BW ignore main.py --dataset deNetwork3_1 --model TTransE --dropout 0.2 --embedding-size 8 --learning-rate 0.01 --epochs 100 --batch-size 32 --test-batch-size 30 --negative-samples 64 --filter --mode head --validation-frequency 2 --threads 2 --workers 1
```
Summary of Horovod & TKGC installation:
```
conda create -n horovod python=3.6
conda install -y openmpi
conda install -y -c cmake
conda install -y -c pytorch pytorch
conda install -y gxx_linux-64
HOROVOD_WITH_PYTORCH=1 pip install -v --no-cache-dir horovod[pytorch]
pip install -r requirements.txt
```

## Converting raw network logs to CSV
1) Amend the `converter/main.py` to use the appropriate dataset converter

Example:
```python
from preprocessing.log2dataset_tkgc
#from preprocessing.log2dataset_tkgcTA
#from preprocessing.log2dataset
```
2) Place the raw network log dataset `conn.log.labeled` that is to be converted
3) Run the script `converter/main.py` to generate `output.csv`
4) 
## Import into Neo4j
### converting the immediate representation to knowledge graph
1) Install Neo4j and create a graph database
2) Place the `output.csv` in the database import folder
3) Run the following cypher command:
```cypher
LOAD CSV FROM "file:///output.csv" as row

CALL apoc.merge.node(['uid'], {id:row[0]}, {})
YIELD node as startNode
CALL apoc.merge.node([row[1]], {id:row[2]}, {})
YIELD node as endNode
CALL apoc.create.relationship(startNode, row[1], {id:row[1]}, endNode) yield rel
RETURN distinct 'done'
```

## Experiment Results
The experiment results for both temporal (Horovod/TKGC) and non-temporal (Ampligraph) models are collated in the `results` folder
