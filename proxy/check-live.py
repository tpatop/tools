import requests
import re
import pyfiglet
from colorama import Fore, Style, init

# Инициализация colorama для поддержки цветов в консоли
init(autoreset=True)

# Выводим ASCII-арт заголовок с желтым цветом
ascii_art = pyfiglet.figlet_format("PROXY CHECKER")
by_text = "By https://t.me/reddragonnodes"
print(f"\n{Fore.YELLOW}{ascii_art}{by_text.center(80)}\n")

# Файл с исходными прокси
proxy_file = "proxies.txt"
test_url = "http://httpbin.org/ip"

# Загружаем прокси из файла
with open(proxy_file) as f:
    proxies_list = f.read().splitlines()

working_proxies = []
working_proxies_auth = []
dead_proxies = []

def clean_proxy(proxy):
    """Удаляет протокол из прокси, если он есть."""
    return re.sub(r'^(http://|https://)', '', proxy, flags=re.IGNORECASE)

cleaned_proxies = list(map(clean_proxy, proxies_list))

for proxy in cleaned_proxies:
    http_proxy = f"http://{proxy}"
    proxies_http = {"http": http_proxy, "https": http_proxy}
    
    try:
        response = requests.get(test_url, proxies=proxies_http, timeout=5, verify=False)
        if response.status_code == 200:
            working_proxies.append(http_proxy)  # Записываем с одним протоколом
            working_proxies_auth.append(proxy)  # Записываем без протокола
            print(f"{Fore.GREEN}✅ Рабочий: {proxy} | Ответ: {response.text.strip()}")
        else:
            dead_proxies.append(proxy)
            print(f"{Fore.RED}❌ Не отвечает: {proxy}")
    except requests.RequestException:
        dead_proxies.append(proxy)
        print(f"{Fore.RED}❌ Ошибка: {proxy}")

# Сохраняем рабочие прокси в формате логин:пароль@адрес:порт
with open("working_proxies_auth_format.txt", "w") as f:
    f.write("\n".join(working_proxies_auth))

# Сохраняем рабочие прокси в формате http://логин:пароль@адрес:порт
with open("working_proxies_http_format.txt", "w") as f:
    f.write("\n".join(working_proxies))

# Сохраняем нерабочие прокси
with open("dead_proxies.txt", "w") as f:
    f.write("\n".join(dead_proxies))

print(f"\n{Fore.YELLOW}Готово! Найдено {len(working_proxies)} рабочих прокси, {len(dead_proxies)} нерабочих.")
