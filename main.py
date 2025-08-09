#!/usr/bin/env python3

import requests
import os
import sys
import time
import threading
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class XSSemoX:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.payloads = []
        self.vulnerable_payloads = []
        self.loading = False
        self.current_wordlist_path = None
        
    def clear_screen(self):
        os.system('clear')
        
    def print_banner(self, title):
        self.clear_screen()
        print(Colors.RED + Colors.BOLD + """
    ╔══════════════════════════════════════╗
    ║         """ + title.center(20) + """         ║
    ╚══════════════════════════════════════╝""")
        print(Colors.RED + """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀ CREATED BY DAVID⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔
⠀⠀⠀⠭⣿⣿⣿⣶⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⡿⠁
⠀⠀⠀⠘⡿⣿⡿⣿⣿⣿⣿⣦⣴⣶⣶⣶⣶⣦⣤⣤⣀⣀⠀⠀⠀⠀⠀⢀⣀⣤⣲⣿⣿⣿⠟⠀⠀
⠀⠀⠀⠀⠐⡝⢿⣌⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣾⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠲⡝⡷⣮⣝⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣿⣿⠿⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣴⣿⣦⣝⠓⠭⣿⡿⢿⣿⣿⣛⠻⣿⠿⠿⣿⣿⣿⣿⣿⣿⡿⣇⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣤⡀⠈⠉⠚⠺⣿⠯⢽⣿⣷⣄⣶⣷⢾⣿⣯⣾⣿⠿⠃⠀⠀⠀⠀⠀⠀
⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⡟⠀⠀⣴⣿⣿⣼⠈⠉⠃⠋⢹⠁⢀⡇⠀⠀⠀⠀⠀⠀
⢠⢿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣀⣀⣀⣀⣴⣿⣿⡿⣿⠀⠀⠀⠀⠇⠀⣼⡇⠀⠀⠀⠀⠀⠀
⠈⠑⢿⢿⣾⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠿⢿⡄⢦⣤⣤⣶⣿⣿⣷⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠙⠘⠛⠋⠁⠁⣀⢉⡉⢻⡻⣯⣻⣿⢻⣿⣀⠀⠀⠀⢠⣾⣿⣿⣿⣹⠉⣍⢁⠀⠀⠀⠀⠀
⠀⠀⣀⠠⠔⠒⠋⠀⡈⠀⠠⠤⠀⠓⠯⣟⣻⣻⠿⠛⠁⠀⠀⠣⢽⣿⡻⠿⠋⠰⠤⣀⡈⠒⢄⠀⠀
⠀⠀⠀⠀⡀⠔⠊⠁⠀⣀⠔⠈⠁⠀⠀⠀⠀⠀⣶⠂⠀⠀⠀⢰⠆⠀⠀⠀⠈⠒⢦⡀⠉⠢⠀⠁⠀
⠀⠀⠀⠊⠀⠀⠀⠀⠎⠁⠀⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠰⠃⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠿⠭⠯⠭⠽⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        """ + Colors.RESET)
        print(Colors.YELLOW + "=" * 40)
        print(Colors.CYAN + "       XSS Pentesting Tool")
        print(Colors.CYAN + "   Lets Fucked Up They're Website!")
        print(Colors.YELLOW + "=" * 40)
        
    def show_progress(self, current, total, vulnerable_found=0):
        chars = "|/-\\"
        char = chars[current % len(chars)]
        percentage = (current / total) * 100
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        status = f"[{char}] Testing payload {current}/{total} ({percentage:.1f}%) [{bar}] Found: {vulnerable_found}"
        print(f"\r{Colors.YELLOW}{status}", end="", flush=True)
        
    def clear_progress_line(self):
        print("\r" + " " * 80 + "\r", end="", flush=True)
        
    def load_wordlist(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(Colors.RED + "[!] File wordlist tidak ditemukan: {}".format(path))
            return []
        except Exception as e:
            print(Colors.RED + "[!] Error membaca file: {}".format(str(e)))
            return []
        
    def test_xss_payload(self, url, payload):
        try:
            # parsing url dan menambahkan payload di param
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            
            # tes payload tiap param
            for param in query_params:
                test_params = query_params.copy()
                test_params[param] = [payload]
                
                # Reconstruct url payload
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    parsed_url.params,
                    new_query,
                    parsed_url.fragment
                ))
                
                # request
                response = self.session.get(test_url, timeout=15)
                
                # cek payload apakah ada reflected respon
                if payload in response.text:
                    # Simple cek potential XSS (not foolproof)
                    if any(tag in payload.lower() for tag in ['<script', '<img', '<svg', '<iframe', 'javascript:', 'onerror', 'onload']):
                        return True, param, test_url
                        
        except Exception as e:
            pass
            
        return False, None, None
        
    def start_attack(self):
        self.print_banner("LetsAttack!")
        print()

        if not self.current_wordlist_path:
            print(Colors.RED + "[!] Wordlist belum dimuat!")
            print(Colors.YELLOW + "[*] Silakan pilih menu 'Input Payload' terlebih dahulu untuk memuat wordlist.")
            input(Colors.CYAN + "\nPress Enter to continue...")
            return
        
        url = input(Colors.CYAN + "Masukkan URL target (contoh: https://example.com/?s=test) : " + Colors.RESET).strip()
        
        if not url:
            print(Colors.RED + "[!] URL tidak boleh kosong!")
            time.sleep(2)
            return
            
        # validasi url
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                print(Colors.RED + "[!] URL tidak valid!")
                time.sleep(2)
                return
        except:
            print(Colors.RED + "[!] URL tidak valid!")
            time.sleep(2)
            return
            
        # Load payloads wl
        self.payloads = self.load_wordlist(self.current_wordlist_path)
        
        if not self.payloads:
            print(Colors.RED + "[!] Tidak ada payload untuk ditest!")
            time.sleep(2)
            return
            
        print(Colors.BLUE + f"[*] Loaded {len(self.payloads)} payloads from: {self.current_wordlist_path}")
        print(Colors.BLUE + f"[*] Testing URL: {url}")
        print()
        
        # real time progres
        self.vulnerable_payloads = []
        total_payloads = len(self.payloads)
        
        print(Colors.BLUE + "[*] Starting XSS payload testing...")
        print()
        
        for i, payload in enumerate(self.payloads, 1):
            self.show_progress(i, total_payloads, len(self.vulnerable_payloads))
            
            vulnerable, param, test_url = self.test_xss_payload(url, payload)
            
            if vulnerable:
                self.clear_progress_line()
                
                vuln_data = {
                    'payload': payload,
                    'parameter': param,
                    'url': test_url
                }
                self.vulnerable_payloads.append(vuln_data)
                
                # Tampilan hasil vukn
                print(Colors.GREEN + f"[VULNERABLE FOUND #{len(self.vulnerable_payloads)}]")
                print(Colors.GREEN + f"Parameter: {param}")
                print(Colors.YELLOW + f"Payload: {payload}")
                print(Colors.BLUE + f"URL: {test_url}")
                print()
                
                self.show_progress(i, total_payloads, len(self.vulnerable_payloads))
            
            
            time.sleep(0.1)
        
        # Clear final progres
        self.clear_progress_line()
        
        # Hasil Final
        print(Colors.BLUE + f"[*] Testing completed!")
        
        if self.vulnerable_payloads:
            print(Colors.GREEN + f"[+] SUMMARY: Found {len(self.vulnerable_payloads)} vulnerable payload(s)")
        else:
            print(Colors.YELLOW + "[*] No vulnerable payloads found")
            
        input(Colors.CYAN + "\nPress Enter to continue...")
        
    def custom_payload_menu(self):
        self.print_banner("XssemoX")
        print()
        
        print(Colors.YELLOW + "[*] Payload sudah disediakan, masukan 'payload.txt' untuk menggunakan payload jika tidak punya custom payload.")
        wordlist_path = input(Colors.CYAN + "Masukan File Payload: " + Colors.RESET).strip()
        
        if not wordlist_path:
            print(Colors.RED + "[!] Path wordlist tidak boleh kosong!")
            time.sleep(2)
            return
            
        if os.path.exists(wordlist_path):
            # Test loading wordlist
            test_payloads = self.load_wordlist(wordlist_path)
            if test_payloads:
                self.current_wordlist_path = wordlist_path
                print(Colors.GREEN + f"[+] Berhasil menggunakan custom file: {wordlist_path}")
                print(Colors.GREEN + f"[+] Loaded {len(test_payloads)} payloads")
            else:
                print(Colors.RED + "[!] File wordlist kosong atau tidak valid!")
        else:
            print(Colors.RED + "[!] File tidak ditemukan!")
            
        time.sleep(3)
        
    def main_menu(self):
        while True:
            self.print_banner("XssemoX")
            print()
            
            # nampilin wordlist status
            if self.current_wordlist_path:
                print(Colors.GREEN + f"[+] Current wordlist: {self.current_wordlist_path}")
            else:
                print(Colors.YELLOW + "[*] No wordlist loaded")
            print()
            
            print(Colors.WHITE + "1. Start Attack")
            print(Colors.WHITE + "2. Input Payload")
            print(Colors.WHITE + "3. Exit")
            print()
            
            try:
                choice = input(Colors.CYAN + "Choose option: " + Colors.RESET).strip()
                
                if choice == "1":
                    self.start_attack()
                elif choice == "2":
                    self.custom_payload_menu()
                elif choice == "3":
                    print(Colors.GREEN + "[+] Thanks for using XssemoX!")
                    sys.exit(0)
                else:
                    print(Colors.RED + "[!] Invalid option!")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(Colors.GREEN + "\n[+] Thanks for using XssemoX!")
                sys.exit(0)
            except Exception as e:
                print(Colors.RED + f"[!] Error: {e}")
                time.sleep(2)

def main():
    # Cek modul requests
    try:
        import requests
    except ImportError:
        print("Error: requests module not found. Install with: pip3 install requests")
        sys.exit(1)
        
    print(Colors.GREEN + "[*] Starting XssemoX...")
    time.sleep(1)
    
    xss_tool = XSSemoX()
    xss_tool.main_menu()

if __name__ == "__main__":
    main()
