[app]
# Título e identificadores
title = Ponto Eletrônico
package.name = pontoeletronico
package.domain = org.example

# Versão
version = 1.0.0

# Fonte
source.dir = .
source.include_exts = py,kv

# Dependências Python (já instaladas no seu .venv)
requirements = python3,kivy==2.3.1,kivymd==1.2.0,python-dateutil>=2.8.2

# Permissões Android
android.permissions = INTERNET

# Orientação / ícone / splash (opcional)
orientation = portrait
# icon.filename = %(source.dir)s/assets/icon.png

# Canais de log mais verbosos para debug
log_level = 2


[buildozer]
# Pasta de build — pode deixar como está
build_dir = ./.buildozer
# Pasta de saída do APK
bin_dir = ./.buildozer/bin


[android]
# Versões do SDK
android.minapi = 21
android.api = 33

# Arquituras suportadas
# armeabi-v7a é suficiente para a maioria; inclua arm64-v8a se quiser
android.arch = armeabi-v7a

# Permite que o Buildozer baixe e instale automaticamente o SDK/NDK,
# se ainda não estiver configurado (em Linux/WSL).
# Não é preciso definir android.sdk_path nem android.ndk_path aqui.
# Se você quiser usar um SDK já instalado, basta definir a variável
# ANDROIDSDK_ROOT ou ANDROID_NDK_HOME no seu ambiente de sistema.

# Exemplo (no Linux/WSL, adicione ao seu ~/.bashrc ou ~/.profile):
# export ANDROIDSDK_ROOT=/home/usuario/Android/Sdk
# export ANDROID_NDK_HOME=/home/usuario/Android/Sdk/ndk/21.4.7075529
