name: Build Android APK
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-20.04  # Naudojame itin stabilią senesnę Ubuntu aplinką
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10' # Pakeičiame į 3.10, kuri idealiai suderinama su žemiau esančiais įrankiais

    - name: Install System Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libsqlite3-dev lld cython3 virtualenv unzip openjdk-17-jdk wget
        # Atsisiunčiame tikslų Android SDK build-tools paketą, kurio trūko
        sudo apt-get install -y android-sdk-build-tools

    - name: Install Buildozer
      run: |
        python -m pip install --upgrade pip
        # Įdiegiame patikrintą 1.4.0 versiją, kuri automatiškai išsprendžia Aidl kelius
        pip install buildozer==1.4.0

    - name: Build with Buildozer
      run: |
        YES=1 buildozer -v android debug
      env:
        ACCEPT_SDK_LICENSE_NET: "y"

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: WorkHoursApp-APK
        path: bin/*.apk
