# Wavelet Detection Filter (WDF) Library
This library contains code for the application of Wavelet Detection Filter (WDF) on the time-series data.
It contains code to estimate Autoregressive parameters for a time serie sequence, and to run whitening and double whitening (equivanentto filter by the inverse of Power Spectral Density) in time domain.

## Getting Started

### Prerequisites

Test up to  Python version = 3.11

Packages:

- numpy
- scipy
- [p4tsa](https://github.com/elenacuoco/p4TSA)
- ...

Alternatively you can download Docker image available [here](https://hub.docker.com/repository/docker/wdfteam/wdfpipe), tagged as `wdfteam/wdfpipe:wdf_env_2.1.1`. To run Docker image you can follow either official Docker [documentation](https://docs.docker.com/get-started/) or follow our official WDF pipeline [manual](https://wdfpipe.gitlab.io/content/manual/).

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running. 

After the installing on env_wdf, you can clone or download master and in wdf directory type: 

```
python setup.py install
```

Test unittest

```
python -m unittest
```

Under the directory examples you can find a bunch of GW data under data/ dir and a few of notebook examples to run and test wdf pipeline or filtering.

### Create Source dist build
To create a source distribution, you run: `python - m build `. It create a tar gz on a directory dist with a source distribution

### Create Binary dist build
To create a binary distribution called a wheel, you run: `python setup.py bdist`

Other opions can be used:
* `python setup.py bdist --formats=rpm` rpm Format
* `python setup.py bdist --formats=wininst` window installer

## Development
Current version - 2.1.1

### Run test
To run the test, enter the 'tests' directory and run one of existing scripts, like: `python -m unittest discover tests/`

### Aligning the code with PEP8 standard
The repository contains pre-commit hooks in order to run formatting and linting checks before the commit process. To run it locally you need to install `pre-commit` Python package. Then each time you run `git commit` the hooks will test your code agaist PEP8 style guide.


### Run Documentation
To create documentation use the `make clean && make docs`. On the directory docs you can see the generated documentation
To run the website go to the _build/html subdirectory. There open `index.html` website.

THe documentation tree is stored in the `index.rst` file and the `structure` directory





## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

 
## Authors

* **Elena Cuoco** - *Author, developer and maintener* - [Elena Cuoco](https://github.com/elenacuoco)
* **Filip Morawski** - *Developer and Maintener* - [Filip Morawski](https://gitlab.com/fmorawski)
* **Alberto Iess** - *Developer and Maintener* - [Alberto Iess](https://gitlab.com/albertoiess)
* **Alessandro Staniscia** - *Contributor* - [Alessandro Staniscia](https://github.com/odyno)



## License

This project is licensed under the GNU General Public License v3.0. License - see the [LICENSE.md](LICENSE) file for details

 