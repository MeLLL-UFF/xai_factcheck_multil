from setuptools import setup, find_packages

setup(
    name='dpr',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'faiss-cpu',
        'tqdm',
        'numpy',
        'scipy',
        'scikit-learn',
        'pandas',
        'ujson',
    ],
    author='Nome do Autor',
    author_email='email@exemplo.com',
    description='Descrição do package dpr',
    url='https://github.com/AkariAsai/CORA/tree/main/mDPR/dpr',
)