[app]

title = Ankeralarm
package.name = ankeralarm
package.domain = gsog.de

icon.filename = Goku.jpg

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,json,txt

version = 0.1
#requirements = python3,kivy,kivymd==1.1.1,pillow,plyer, requests, openssl, urllib3, mapview, kivy_garden, charset_normalizer, chardet
requirements = appdirs==1.4.4,asgiref==3.7.2,asttokens==2.4.1,black==22.12.0,certifi==2023.11.17,charset-normalizer==3.3.2,click==8.1.7,colorama==0.4.6,contourpy==1.2.0,coverage==7.4.0,cycler==0.12.1,debugpy==1.8.0,decorator==5.1.1,dj-database-url==1.3.0,Django==4.2.9,django-widget-tweaks==1.5.0,docutils==0.20.1,executing==2.0.1,ffmpeg==1.4,filelock==3.13.1,fonttools==4.49.0,frozendict==2.4.0,fsspec==2023.12.2,gunicorn==20.1.0,hiredis==2.3.2,honcho==1.1.0,html5lib==1.1,hupper==1.12,idna==3.6,iniconfig==2.0.0,ipython==8.20.0,jedi==0.19.1,Jinja2==3.1.3,Kivy==2.3.0,kivy-deps.angle==0.4.0,kivy-deps.glew==0.3.1,kivy-deps.sdl2==0.7.0,Kivy-examples==2.3.0,Kivy-Garden==0.1.5,kivy-garden.mapview==1.0.6,kivymd==1.1.1,kiwisolver==1.4.5,lxml==5.1.0,mapview==1.0.6,MarkupSafe==2.1.4,matplotlib==3.8.3,matplotlib-inline==0.1.6,mpmath==1.3.0,multitasking==0.0.11,mutagen==1.47.0,mypy-extensions==1.0.0,networkx==3.2.1,numpy==1.26.3,packaging==23.2,pandas==2.1.4,parso==0.8.3,pathspec==0.12.1,peewee==3.17.0,pillow==10.2.0,platformdirs==4.1.0,pluggy==1.4.0,plyer==2.1.0,prompt-toolkit==3.0.43,psycopg2-binary==2.9.9,pure-eval==0.2.2,pycairo==1.25.1,Pygments==2.17.2,pyparsing==3.1.1,pypiwin32==223,pytest==7.4.4,pytest-django==4.7.0,python-dateutil==2.8.2,python-dotenv==0.20.0,pytz==2023.3.post1,pywin32==306,redis==4.6.0,requests==2.31.0,ruff==0.0.194,six==1.16.0,soupsieve==2.5,sqlparse==0.4.4,stack-data==0.6.3,sympy==1.12,traitlets==5.14.1,typing_extensions==4.9.0,tzdata==2023.4,urllib3==2.1.0,wcwidth==0.2.13,webencodings==0.5.1,whitenoise==6.6.0,yfinance==0.2.35


orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
p4a.branch = release-2022.12.20

android.permissions = INTERNET

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

[buildozer]
log_level = 2
warn_on_root = 1
