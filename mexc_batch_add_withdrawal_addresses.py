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
      await delay(400); // Ждем, чтобы строка добавилась
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
  coinInput = row.querySelector('input[id*="coinId"]') || 
             coinInputs[1];
  
  if (coinInput) {{
    console.log(`Заполняем поле монеты (${{coinValue}})`);
    setReactInputValue(coinInput, coinValue);
    
    // Триггерим события для открытия выпадающего списка
    coinInput.focus();
    coinInput.click();
    
    // Даем время на открытие списка
    await delay(500);
    
    // Ищем выпадающий список, связанный с текущим полем
    // Обычно Ant Design создает dropdown в конце body
    const dropdowns = document.querySelectorAll('.ant-select-dropdown:not(.ant-select-dropdown-hidden)');
    const lastDropdown = dropdowns[dropdowns.length - 1]; // Берем последний открытый dropdown
    
    if (lastDropdown) {{
      const coinOptions = lastDropdown.querySelectorAll('.ant-select-item.ant-select-item-option');
      console.log(`Найдено ${{coinOptions.length}} опций монет в текущем dropdown`);
      
      if (coinOptions.length > 0) {{
        // Ищем соответствующую опцию или берем первую
        const targetOption = Array.from(coinOptions).find(opt => 
          opt.textContent.includes(coinValue)
        ) || coinOptions[0];
        
        console.log(`Выбираем опцию: ${{targetOption.textContent}}`);
        
        // Убеждаемся, что опция видима
        targetOption.scrollIntoView({{ block: 'nearest' }});
        await delay(100);
        
        // Кликаем по опции
        targetOption.click();
        await delay(300);
      }}
    }} else {{
      console.error("Выпадающий список не найден");
      
      // Альтернативный подход - симулируем нажатие клавиш
      const event = new KeyboardEvent('keydown', {{ 
        key: 'Enter', 
        keyCode: 13, 
        which: 13,
        bubbles: true 
      }});
      coinInput.dispatchEvent(event);
    }}
  }} else {{
    console.error("Поле для монеты не найдено");
  }}
}}
  await delay(300);

// 2. Заполняем сеть (по второму combobox rc_select_* и его aria-controls)
try {{
  // Находим все combobox-инпуты в текущей строке
  const comboInputs = Array.from(
    row.querySelectorAll('input.ant-select-selection-search-input[role="combobox"][id^="rc_select_"]')
  );

  if (comboInputs.length === 0) {{
    console.error('В текущей строке combobox-инпуты не найдены');
  }} else {{
    // Берём "второй" combobox в строке (обычно это — Сеть)
    const networkInput = comboInputs[1] || comboInputs[0];

    if (!networkInput) {{
      console.error('Поле ввода для сети не найдено');
    }} else {{
      console.log(`Заполняем поле сети (${{networkValue}}), input.id=${{networkInput.id}}`);
      setReactInputValue(networkInput, networkValue);

      // Откроем dropdown для именно этого инпута
      networkInput.focus();
      networkInput.click();
      await delay(400);

      // Ждем dropdown, связанный с этим инпутом, по aria-controls / aria-owns
      const controlsId = networkInput.getAttribute('aria-controls') || networkInput.getAttribute('aria-owns');

      const waitForDropdownByInput = (input, timeout = 5000) =>
        new Promise((resolve, reject) => {{
          const targetId = input.getAttribute('aria-controls') || input.getAttribute('aria-owns');
          const started = Date.now();

          const tryFind = () => {{
            if (!targetId) return null;
            const listEl = document.getElementById(targetId);
            if (listEl) {{
              const dropdown = listEl.closest('.ant-select-dropdown');
              if (dropdown && !dropdown.classList.contains('ant-select-dropdown-hidden')) {{
                return {{ listEl, dropdown }};
              }}
            }}
            return null;
          }};

          const first = tryFind();
          if (first) return resolve(first);

          const obs = new MutationObserver(() => {{
            const found = tryFind();
            if (found) {{
              obs.disconnect();
              resolve(found);
            }} else if (Date.now() - started > timeout) {{
              obs.disconnect();
              reject(new Error('Timeout waiting for dropdown'));
            }}
          }});

          obs.observe(document.body, {{ childList: true, subtree: true }});
          setTimeout(() => {{
            obs.disconnect();
            reject(new Error('Timeout waiting for dropdown'));
          }}, timeout);
        }});

      let dropdownCtx = null;
      try {{
        dropdownCtx = await waitForDropdownByInput(networkInput, 5000);
      }} catch (e) {{
        console.warn('Не дождались dropdown по aria-controls, пробуем фолбэк на последний открытый:', e);
      }}

      // Если не нашли по связке — фолбэк: берем последний видимый dropdown
      const dropdown =
        dropdownCtx?.dropdown ||
        Array.from(document.querySelectorAll('.ant-select-dropdown:not(.ant-select-dropdown-hidden)')).pop();

      if (dropdown) {{
        const optionNodes = dropdown.querySelectorAll('.ant-select-item.ant-select-item-option');
        console.log(`Найдено ${{optionNodes.length}} опций сети в связанном dropdown (controls=${{controlsId || 'n/a'}})`);

        if (optionNodes.length > 0) {{
          const options = Array.from(optionNodes);

          // Ищем непустую и не disabled опцию по тексту (case-insensitive)
          const lcValue = String(networkValue || '').trim().toLowerCase();
          const targetOption =
            options.find(opt => {{
              const text = opt.textContent?.trim().toLowerCase() || '';
              const disabled = opt.classList.contains('ant-select-item-option-disabled');
              return !disabled && (lcValue ? text.includes(lcValue) : true);
            }}) ||
            options.find(opt => !opt.classList.contains('ant-select-item-option-disabled')) ||
            options[0];

          console.log(`Выбираем опцию сети: ${{targetOption?.textContent?.trim() || '(первая доступная)'}} `);
          targetOption.scrollIntoView({{ block: 'nearest' }});
          await delay(200);
          targetOption.click();
          await delay(400);
        }} else {{
          console.warn('Опции сети не найдены в dropdown — подтверждаем Enter');
          networkInput.dispatchEvent(new KeyboardEvent('keydown', {{
            key: 'Enter', keyCode: 13, which: 13, bubbles: true
          }}));
        }}
      }} else {{
        console.error('Выпадающий список сети не найден — фолбэк Enter');
        networkInput.dispatchEvent(new KeyboardEvent('keydown', {{
          key: 'Enter', keyCode: 13, which: 13, bubbles: true
        }}));
      }}
    }}
  }}
}} catch (e) {{
  console.error('Ошибка при заполнении сети:', e);
}}

await delay(300);

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
      await delay(500); // Ждем, чтобы все строки загрузились
    }}

    // Теперь заполняем каждую строку
    for (let i = 0; i < walletAddresses.length; i++) {{
      await fillRow(i, "{COIN}", "{NETWORK}", walletNames[i], walletAddresses[i]);
      await delay(200); // Задержка между заполнением строк
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
    
