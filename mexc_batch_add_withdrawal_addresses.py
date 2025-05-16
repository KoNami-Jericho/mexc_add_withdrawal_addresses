import json

COIN = "ETH"
NETWORK = "BASE"

with open('wallet_addresses.txt') as f:
    wallet_addresses = f.readlines()
    wallet_addresses = [wallet.strip('\n') for wallet in wallet_addresses]

with open('wallet_names.txt') as f:
    wallet_names = f.readlines()
    wallet_names = [name.strip('\n') for name in wallet_names]

assert len(wallet_addresses) == len(wallet_names), "Длина списков должна совпадать"

# Преобразуем массивы Python в строки, пригодные для JavaScript
js_wallet_names = json.dumps(wallet_names)
js_wallet_addresses = json.dumps(wallet_addresses)

# Универсальная JS-функция с полностью новым подходом
init_script = f'''
// Данные кошельков
const walletNames = {js_wallet_names};
const walletAddresses = {js_wallet_addresses};

// Используем промисы для последовательного выполнения с задержками
function delay(ms) {{
  return new Promise(resolve => setTimeout(resolve, ms));
}}

// Функция для установки значений в React-компоненты
function setReactInputValue(el, value) {{
  if (!el) return false;

  const lastValue = el.value;
  el.focus();
  el.value = value;

  // Обработка React трекера значений
  const tracker = el._valueTracker;
  if (tracker) {{
    tracker.setValue(lastValue);
  }}

  // Отправка событий React
  el.dispatchEvent(new Event('input', {{ bubbles: true }}));
  el.dispatchEvent(new Event('change', {{ bubbles: true }}));

  return true;
}}

// Функция для добавления нужного количества строк
async function addRows(count) {{
  console.log(`Добавляем ${{count}} новых строк...`);
  const addButton = document.querySelector("#__next > div.withdraw-address-batch-add_withdrawAddressBatchAdd__MiMpl > div > div.withdraw-address-batch-add_commonItem__c4gNO > div.withdraw-address-batch-add_addOneAddressFormItem__Dh8Yr > div > span");

  for (let i = 2; i < count; i++) {{
    console.log(`Добавляем строку ${{i}} + 1}}/${{count}}`);
    if (addButton) {{
      addButton.click();
      await delay(700); // Ждем, чтобы строка добавилась
    }} else {{
      console.error("Кнопка добавления не найдена");
      break;
    }}
  }}

  console.log("Добавление строк завершено");
  return true;
}}

// Функция для заполнения строки (более точный поиск элементов)
async function fillRow(rowIndex, coinValue, networkValue, nameValue, addressValue) {{
  console.log(`Заполняем строку ${{rowIndex}}...`);

  // Ищем все строки на странице
  const rows = Array.from(document.querySelectorAll('.ant-row')).filter(row => {{
    // Отфильтровываем только строки с формами (содержащие input и select)
    return row.querySelectorAll('input').length >= 3;
  }});

  if (rowIndex >= rows.length) {{
    console.error(`Строка ${{rowIndex}} не найдена. Доступно только ${{rows.length}} строк.`);
    return false;
  }}

  const row = rows[rowIndex];
  console.log(`Найдена строка ${{rowIndex}}`);

  // 1. Заполняем монету
  const coinInputs = row.querySelectorAll('input');
  let coinInput;

  // Ищем поле для монеты (обычно 2-й инпут)
  if (coinInputs.length >= 2) {{
    // В разных случаях это может быть разный элемент, поэтому пробуем несколько вариантов
    coinInput = row.querySelector('input[id*="coinId"]') || 
               coinInputs[1];

    if (coinInput) {{
      console.log(`Заполняем поле монеты (${{coinValue}})`);
      setReactInputValue(coinInput, coinValue);
      await delay(300);

      // Клик по опции в выпадающем списке
      const coinOptions = document.querySelectorAll('.ant-select-item.ant-select-item-option');
      console.log(`Найдено ${{coinOptions.length}} опций монет`);

      if (coinOptions.length > 0) {{
        // Ищем соответствующую опцию или берем первую
        const targetOption = Array.from(coinOptions).find(opt => 
          opt.textContent.includes(coinValue)
        ) || coinOptions[0];

        console.log(`Выбираем опцию: ${{targetOption.textContent}}`);
        targetOption.click();
      }}
    }} else {{
      console.error("Поле для монеты не найдено");
    }}
  }}

  await delay(800);

  // 2. Заполняем сеть
  const networkInputs = document.querySelectorAll('.ant-select-selection-search-input');

  // Получаем все контейнеры выбора сети в текущей строке
  const networkContainers = row.querySelectorAll('.ant-select-selection-search');

  if (networkContainers.length > 0) {{
    // Берем второй контейнер (первый обычно для монеты, второй для сети)
    const networkContainer = networkContainers[1] || networkContainers[0];
    if (networkContainer) {{
      const networkInput = networkContainer.querySelector('input');

      if (networkInput) {{
        console.log(`Заполняем поле сети (${{networkValue}})`);
        setReactInputValue(networkInput, networkValue);
        await delay(300);

        // Клик по опции в выпадающем списке
        const networkOptions = document.querySelectorAll('.ant-select-item.ant-select-item-option');

        if (networkOptions.length > 0) {{
          // Ищем соответствующую опцию или берем первую
          const targetOption = Array.from(networkOptions).find(opt => 
            opt.textContent.includes(networkValue)
          ) || networkOptions[0];

          console.log(`Выбираем опцию сети: ${{targetOption.textContent}}`);
          targetOption.click();
        }}
      }} else {{
        console.error("Поле ввода для сети не найдено");
      }}
    }} else {{
      console.error("Контейнер для выбора сети не найден");
    }}
  }}

  await delay(800);

  // 3. Заполняем имя и адрес
  const remarkInput = row.querySelector('input[id*="remark"]') || coinInputs[3]; 
  const addressInput = row.querySelector('input[id*="address"]') || coinInputs[4];

  if (remarkInput) {{
    console.log(`Заполняем имя кошелька (${{nameValue}})`);
    setReactInputValue(remarkInput, nameValue);
  }} else {{
    console.error("Поле для имени не найдено");
  }}

  if (addressInput) {{
    console.log(`Заполняем адрес кошелька (${{addressValue}})`);
    setReactInputValue(addressInput, addressValue);
  }} else {{
    console.error("Поле для адреса не найдено");
  }}

  console.log(`Строка ${{rowIndex}} заполнена`);
  return true;
}}

// Основная функция для выполнения всей автоматизации
async function autoFillAllRows() {{
  try {{
    console.log("Начинаем автоматическое заполнение...");

    // Сначала добавляем нужное количество строк (минус 1, так как одна строка уже есть)
    const rowsToAdd = walletAddresses.length - 1;

    if (rowsToAdd > 0) {{
      await addRows(rowsToAdd);
      await delay(1000); // Ждем, чтобы все строки загрузились
    }}

    // Теперь заполняем каждую строку
    for (let i = 0; i < walletAddresses.length; i++) {{
      await fillRow(i, "{COIN}", "{NETWORK}", walletNames[i], walletAddresses[i]);
      await delay(1000); // Задержка между заполнением строк
    }}

    console.log("Автоматическое заполнение завершено!");
  }} catch (error) {{
    console.error("Произошла ошибка при автоматизации:", error);
  }}
}}

// Запускаем процесс автоматизации
autoFillAllRows();
'''

# Итоговый JS
print(init_script)
with open('wallet_add.js.txt', 'w', encoding="utf-8") as f:
    f.write(init_script)
    