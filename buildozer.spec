[app]
title = Zurna Search
package.name = zurnasearch
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# 8. satır civarında hata veren "user" kısmını sildik, yerine bunu yazdık:
requirements = python3,kivy,requests,urllib3,certifi

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
