import requests
import re
import pyfiglet
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

# Инициализация colorama для поддержки цветов в консоли
init(autoreset=True)

def print_banner():
    """Выводим ASCII-арт заголовок с желтым цветом."""
    ascii_art = pyfiglet.figlet_format("PROXY CHECKER")
    by_text = "By https://t.me/reddragonnodes"
    print(f"\n{Fore.YELLOW}{ascii_art}{by_text.center(80)}\n")

def load_proxies(file_path):
    """Загружает прокси из файла."""
    with open(file_path) as f:
        return f.read().splitlines()

def clean_proxy(proxy):
    """Удаляет протокол из прокси, если он есть."""
    return re.sub(r'^(http://|https://)', '', proxy, flags=re.IGNORECASE)

def check_proxy(proxy, test_url):
    """Проверяет работоспособность прокси."""
    http_proxy = f"http://{proxy}"
    proxies_http = {"http": http_proxy, "https": http_proxy}
    
    try:
        response = requests.get(test_url, proxies=proxies_http, timeout=5, verify=False)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅✅✅ {proxy}")
            return proxy, http_proxy, True
        else:
            print(f"{Fore.RED}❓❓❓ {proxy}")
            return proxy, None, False
    except requests.RequestException:
        print(f"{Fore.RED}❌❌❌ {proxy}")
        return proxy, None, False

def save_proxies(file_path, proxies):
    """Сохраняет список прокси в файл."""
    with open(file_path, "w") as f:
        f.write("\n".join(proxies))

def main():
    # Основные параметры
    proxy_file = "working_proxies.txt"
    test_url = "http://httpbin.org/ip"
    output_files = {
        "auth": "working_proxies_auth_format.txt",
        "http": "working_proxies_http_format.txt",
        "dead": "dead_proxies.txt",
    }

    # Выводим баннер
    print_banner()

    # Загружаем прокси
    proxies_list = load_proxies(proxy_file)
    cleaned_proxies = list(map(clean_proxy, proxies_list))

    # Списки для хранения результатов
    working_proxies = []
    working_proxies_auth = []
    dead_proxies = []

    # Проверяем прокси в многопоточном режиме
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_proxy, proxy, test_url) for proxy in cleaned_proxies]
        
        for future in as_completed(futures):
            proxy, http_proxy, is_working = future.result()
            if is_working:
                working_proxies_auth.append(proxy)
                working_proxies.append(http_proxy)
            else:
                dead_proxies.append(proxy)

    # Сохраняем результаты
    save_proxies(output_files["auth"], working_proxies_auth)
    save_proxies(output_files["http"], working_proxies)
    save_proxies(output_files["dead"], dead_proxies)

    # Выводим итоговый отчет
    print(f"\n{Fore.YELLOW}Готово! Найдено {len(working_proxies)} рабочих прокси, {len(dead_proxies)} нерабочих.")

if __name__ == "__main__":
    main()
