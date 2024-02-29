[app]

title = Ankeralarm
package.name = ankeralarm
package.domain = gsog.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,json,txt

version = 0.1
requirements = python3,kivy,kivymd==1.1.1,pillow,plyer, requests, openssl, urllib3, mapview, kivy_garden, charset_normalizer, chardet, idna


# (list) Permissions
android.permissions = INTERNET,ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
p4a.branch = release-2022.12.20

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

[buildozer]
log_level = 2
