# Additional Services

## Prerequisites

- python
- mongodb

### Installation

Install MongoDB.

```bash
pip install -r requirements.txt
```

### Usage

```bash
# launch and setup MongoDB
sudo mongod --bind_ip localhost --replSet services_set --port 27017 --dbpath ./data/db1
sudo mongod --bind_ip localhost --replSet services_set --port 28017 --dbpath ./data/db2
sudo mongod --bind_ip localhost --replSet services_set --port 29017 --dbpath ./data/db3
python setup.py

# launch the service (can specify address through uvicorn)
uvicorn app:app
```
