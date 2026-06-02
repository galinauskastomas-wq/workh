[app]
title = WorkHoursApp
package.name = workhoursapp
package.domain = org.tomas
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0
requirements = python3==3.11.9,kivy==2.3.0,hostpython3==3.11.9
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = armeabi-v7a, arm64-v8a
android.release_artifact = apk
android.debug_artifact = apk
