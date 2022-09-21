# Установка

## Клиент

1. Установить [Flutter](https://docs.flutter.dev/get-started/install/linux)

2. (Опционально) Установить [Android Studio](https://developer.android.com/studio)

3. Установить [SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)

4. Прописать в консоли `adb reverse tcp:порт tcp:порт` для порта, на котором будет работать сервер

5. Сомпилировать проект из папки `client`

## Сервер

1. Поместить файлы с весами моделей в папку `app/weights`

2. Создать докер контейнер `bash build.sh`

3. Запустить контейнер `bash up.sh`

4. Запустить внутри контейнера `bash run.sh`, при желании изменив порт
