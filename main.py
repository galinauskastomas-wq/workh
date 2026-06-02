name: Build Android APK
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libsqlite3-dev lld cython3 virtualenv unzip
        python -m pip install --upgrade pip
        pip install "buildozer>=1.5.0"

    - name: Build with Buildozer
      run: |
        YES=1 buildozer -v android debug

