# Deep Snake

A snake game made in Pygame 2 that will be used to train a neural network AI that will eventually take control over snake.

![Screenshot of Deep Snake](screenshot.png "Screenshot of Deep Snake")

## Prequisites

- Python 3.9
- Pygame 2 ( `pip install pygame==2.0.0` )
- Numpy (`pip install numpy`)
- Tensorflow
- Sklearn
- Matplotlib
- OpenAI Gym (`pip install gym`)

### Mac M1

For Mac M1, follow [these instructions](https://mobiarch.wordpress.com/2021/09/24/installing-tensorflow-in-macos-m1-chip/)

Or, in short:

```sh
brew install miniforge
conda init zsh
conda activate # perhaps restart terminal
which python # should be: /opt/homebrew/Caskroom/miniforge/base/bin/python
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
conda install -c apple tensorflow-deps
python -m pip install tensorflow-macos
python -m pip install tensorflow-metal
conda install pandas scikit-learn numpy
python -m pip install matplotlib jupyterlab
```

## Run Deep Snake

```sh
python main.py
```
