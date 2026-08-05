# ZapretLauncher 

Простой и красивый лаунчер для управления сервисом **Zapret** (версия 1.9.8c).

## Возможности 

*   **Запуск стратегий:** Выбор и запуск любого `.bat` файла из папки с программой.
*   **Управление сервисом:** Установка, удаление и проверка статуса сервиса `zapret`.
*   **Настройки:** Открытие `service.bat` с удобной подсказкой по командам.
*   **Обновления:** Встроенная проверка новых версий на GitHub.
*   **Красивый интерфейс:** Тёмная тема на базе `customtkinter`.

## Установка и запуск 

1.  Скачайте последнюю версию `ZapretLauncher.exe` со страницы [Releases](https://github.com/dimacmirnov41-netizen/ZapretLauncher/releases).
2.  Поместите файл в папку с распакованным **Zapret** (рядом с `service.bat` и папками `bin`, `lists`, `utils`).
3.  Запустите `ZapretLauncher.exe` от имени администратора.

## Сборка из исходников 

1.  Клонируйте репозиторий.
2.  Установите зависимости: `pip install customtkinter requests`
3.  Соберите `.exe` файл:
    ```bash
    pyinstaller --onefile --noconsole --name "ZapretLauncher" --icon=icon.ico zapret_gui.py
