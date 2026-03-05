[app]
title = Zurna Search
package.name = zurnasearch
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Gereklilikler
requirements = python3,kivy,requests,urllib3,certifi

# İzinler
android.permissions = INTERNET

# Samsung A17 için Hedef Ayarlar
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# KRİTİK NOKTA: Sadece senin telefonun için tek mimari
android.archs = arm64-v8a

# Lisans kabulü (Hata vermemesi için)
android.accept_sdk_license = True
