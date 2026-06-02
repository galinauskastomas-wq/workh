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

    - name: Install System Dependencies
      run: |
        sudo apt-get update
        # Pridedame papildomus įrankius: autoconf, automake, libtool, patch
        sudo apt-get install -y libsqlite3-dev lld cython3 virtualenv unzip openjdk-17-jdk wget autoconf automake libtool patch
        python -m pip install --upgrade pip
        pip install "buildozer>=1.5.0"

    - name: Build with Buildozer
      run: |
        # Suteikiame pilnas teises aplankui prieš pradedant darbą
        chmod -R 777 .
        YES=1 buildozer -v android debug
      env:
        ACCEPT_SDK_LICENSE_NET: "y"

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: WorkHoursApp-APK
        path: bin/*.apk
