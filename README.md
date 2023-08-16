# Test Improvado
## Tested on
**Docker**: 24.0.2  
**OS**: MacOS 13.4.1  
**CPU**: ARM64

## Prepare

```
git clone git@github.com:smokfyz/test-improvado.git
cd ./test-improvado
docker build -t test-improvado .
```

## Run simulation
You can find some simulation parameters in `main.py`'s global variables.
```
docker run --rm -v $(PWD):/app test-improvado python main.py
```

## Run tests
```
docker run --rm -v $(PWD):/app test-improvado pytest --cov=./elevator tests/
```
