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
        sudo apt-get install -y libsqlite3-dev lld cython3 virtualenv unzip openjdk-17-jdk wget aidl
        python -m pip install --upgrade pip
        pip install "buildozer>=1.5.0"

    - name: Pre-create Buildozer SDK and Aidl path
      run: |
        # Šis žingsnis priverstinai sukuria aplanką, kurio trūkumą rodė klaida
        mkdir -p /home/runner/.buildozer/android/platform/android-sdk/build-tools/34.0.0
        # Įkopijuojame sistemos aidl programą tiesiai į Buildozer laukiamą vietą
        cp /usr/bin/aidl /home/runner/.buildozer/android/platform/android-sdk/build-tools/34.0.0/aidl
        chmod +x /home/runner/.buildozer/android/platform/android-sdk/build-tools/34.0.0/aidl
        echo "Aidl failas sėkmingai paruoštas vietoje!"

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

