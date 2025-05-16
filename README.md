Адреса построчно в файл `wallet_addresses.txt`  
Имена в `wallet_names.txt`   

В `mexc_batch_add_withdrawal_addresses.py` сверху укажите в `COIN` и `NETWORK` название монеты и сети так, как они отображаются капсом в выпадающих меню на сайте.  

Запуск:  
`py mexc_batch_add_withdrawal_addresses.py`

Результат будет сохранен в файл `wallet_add.js.txt`  
Скопируйте все его содержимое, откройте в Chrome `DevTools`, нажав `Ctrl+Shift+I`, перейдите во вкладку `Console`, вставьте в поле ввода скопированный скрипт и нажмите `Enter`  