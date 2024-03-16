from setuptools import setup, find_packages

setup(
    name='qosfmentorshipjosefinacresta',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'qiskit==1.0.2',
        'numpy==1.26.4',
        'matplotlib==3.8.0',
        'jupyter',
        'ipykernel'
    ],
    python_requires='>=3.7',
)