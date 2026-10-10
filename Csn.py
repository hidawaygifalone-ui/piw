# EyeXscan - Cyberpunk Edition
# Original obfuscated by Mr.X | Redesigned theme: Cyberpunk
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.live import Live
from rich.panel import Panel
from rich.style import Style
from rich.align import Align
from rich.text import Text
import requests
import socket
import ssl
import whois
import dns.resolver
from datetime import datetime
import urllib.parse
import time
import concurrent.futures
import os
import platform
import pyfiglet

# ==================== CYBERPUNK COLOR PALETTE ====================
COLORS = {
    'primary':    '#ff2a6d',   # Neon Magenta / Hot Pink
    'secondary':  '#05d9e8',   # Electric Cyan
    'accent':     '#d1f7ff',   # Ice Blue
    'success':    '#00ff9f',   # Neon Green
    'warning':    '#f9f002',   # Electric Yellow
    'error':      '#ff3864',   # Cyber Red
    'info':       '#05d9e8',   # Cyan
    'text':       '#c9d1d9',   # Soft Grey
    'highlight':  '#ff2a6d',   # Magenta
    'dim':        '#6e7681',   # Dim Grey
    'bg':         '#0d0221',   # Deep Purple Black
}

console = Console()

# ==================== ASCII BANNER ====================
ASCII_BANNER = """⠀⠀⠀⠀⡀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⠉⣹⠋⠉⢉⡟⢩⢋⠋⣽⡻⠭⢽⢉⠯⠭⠭⠭⢽⡍⢹⡍⠙⣯⠉⠉⠉⠉⠉⣿⢫⠉⠉⠉⢉⡟⠉⢿⢹⠉⢉⣉⢿⡝⡉⢩⢿⣻⢍⠉⠉⠩⢹⣟⡏⠉⠹⡉⢻⡍⡇
⠀⢸⢠⢹⠀⠀⢸⠁⣼⠀⣼⡝⠀⠀⢸⠘⠀⠀⠀⠀⠈⢿⠀⡟⡄⠹⣣⠀⠀⠐⠀⢸⡘⡄⣤⠀⡼⠁⠀⢺⡘⠉⠀⠀⠀⠫⣪⣌⡌⢳⡻⣦⠀⠀⢃⡽⡼⡀⠀⢣⢸⠸⡇
⠀⢸⡸⢸⠀⠀⣿⠀⣇⢠⡿⠀⠀⠀⠸⡇⠀⠀⠀⠀⠀⠘⢇⠸⠘⡀⠻⣇⠀⠀⠄⠀⡇⢣⢛⠀⡇⠀⠀⣸⠇⠀⠀⠀⠀⠀⠘⠄⢻⡀⠻⣻⣧⠀⠀⠃⢧⡇⠀⢸⢸⡇⡇
⠀⢸⡇⢸⣠⠀⣿⢠⣿⡾⠁⠀⢀⡀⠤⢇⣀⣐⣀⠀⠤⢀⠈⠢⡡⡈⢦⡙⣷⡀⠀⠀⢿⠈⢻⣡⠁⠀⢀⠏⠀⠀⠀⢀⠀⠄⣀⣐⣀⣙⠢⡌⣻⣷⡀⢹⢸⡅⠀⢸⠸⡇⡇
⠀⢸⡇⢸⣟⠀⢿⢸⡿⠀⣀⣶⣷⣾⡿⠿⣿⣿⣿⣿⣿⣶⣬⡀⠐⠰⣄⠙⠪⣻⣦⡀⠘⣧⠀⠙⠄⠀⠀⠀⠀⠀⣨⣴⣾⣿⠿⣿⣿⣿⣿⣿⣶⣯⣿⣼⢼⡇⠀⢸⡇⡇⡇
⠀⢸⢧⠀⣿⡅⢸⣼⡷⣾⣿⡟⠋⣿⠓⢲⣿⣿⣿⡟⠙⣿⠛⢯⡳⡀⠈⠓⠄⡈⠚⠿⣧⣌⢧⠀⠀⠀⠀⠀⣠⣺⠟⢫⡿⠓⢺⣿⣿⣿⠏⠙⣏⠛⣿⣿⣾⡇⢀⡿⢠⠀⡇
⠀⢸⢸⠀⢹⣷⡀⢿⡁⠀⠻⣇⠀⣇⠀⠘⣿⣿⡿⠁⠐⣉⡀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠳⠄⠀⠀⠀⠀⠋⠀⠘⡇⠀⠸⣿⣿⠟⠀⢈⣉⢠⡿⠁⣼⠁⣼⠃⣼⠀⡇
⠀⢸⠸⣀⠈⣯⢳⡘⣇⠀⠀⠈⡂⣜⣆⡀⠀⠀⢀⣀⡴⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢽⣆⣀⠀⠀⠀⣀⣜⠕⡊⠀⣸⠇⣼⡟⢠⠏⠀⡇
⠀⢸⠀⡟⠀⢸⡆⢹⡜⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠋⣾⡏⡇⡎⡇⠀⡇
⠀⢸⠀⢃⡆⠀⢿⡄⠑⢽⣄⠀⠀⠀⢀⠂⠠⢁⠈⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠄⡐⢀⠂⠀⠀⣠⣮⡟⢹⣯⣸⣱⠁⠀⡇
⠀⠈⠉⠉⠋⠉⠉⠋⠉⠉⠉⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠋⡟⠉⠉⡿⠋⠋⠋⠉⠉⠁"""

# ==================== UTILITIES ====================
def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def clean_url(url):
    url = url.strip().lower()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def get_domain(url):
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc

def format_date(date_str):
    if not date_str:
        return "Not Available"
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str, "%b %d %H:%M:%S %Y GMT")
        else:
            date_obj = date_str
        return date_obj.strftime("%d %B %Y")
    except Exception:
        return str(date_str)

def get_security_headers(headers):
    security_headers = {
        'Strict-Transport-Security': 'HSTS',
        'Content-Security-Policy': 'CSP',
        'X-Frame-Options': 'X-Frame',
        'X-Content-Type-Options': 'X-Content-Type',
        'X-XSS-Protection': 'XSS Protection',
        'Referrer-Policy': 'Referrer Policy',
        'Feature-Policy': 'Feature Policy'
    }
    return {new_name: headers.get(header, 'Not Available')
            for header, new_name in security_headers.items()}

# ==================== SCANNERS ====================
def check_admin_panel(url, timeout=3):
    admin_paths = ['/admin', '/administrator', '/wp-admin', '/login',
                   '/panel', '/admin.php', '/admin/login', '/cp']
    found_paths = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        def check_path(path):
            try:
                test_url = url.rstrip('/') + path
                response = requests.get(test_url, timeout=timeout, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    return test_url
            except:
                pass
            return None

        futures = [executor.submit(check_path, path) for path in admin_paths]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                found_paths.append(future.result())

    return found_paths

def grab_banner(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        server = response.headers.get('Server', 'Not Available')
        x_powered_by = response.headers.get('X-Powered-By', 'Not Available')
        return server, x_powered_by
    except Exception as e:
        return f'Error: {str(e)}', 'Not Available'

def get_technologies(url):
    try:
        response = requests.get(url)
        return "Analysis not implemented"
    except:
        return "Not Available"

def get_server_location(url):
    try:
        response = requests.get(url)
        server_ip = response.raw._connection.sock.getpeername()[0]
        location = requests.get(f"https://ipinfo.io/{server_ip}/json").json()
        return location.get("city", "Not Available"), location.get("country", "Not Available")
    except:
        return "Not Available", "Not Available"

# ==================== UI ====================
def create_styled_table(title):
    table = Table(
        title=f"[bold {COLORS['primary']}]◤ {title} ◢[/]",
        title_style=Style(color=COLORS['primary'], bold=True),
        border_style=Style(color=COLORS['secondary']),
        header_style=Style(color=COLORS['accent'], bold=True),
        pad_edge=False,
        expand=True,
        show_lines=True
    )
    table.add_column(f"[{COLORS['warning']}]▓ CATEGORY[/]",
                     style=Style(color=COLORS['warning'], bold=True), no_wrap=True)
    table.add_column(f"[{COLORS['text']}]▓ DETAILS[/]",
                     style=Style(color=COLORS['text']))
    return table

def show_banner():
    clean_screen()
    banner_text = Text(ASCII_BANNER, style=f"bold {COLORS['primary']}")
    console.print(Panel(
        Align.center(banner_text),
        title=f"[bold {COLORS['secondary']}]▚▚ EYE X SCAN ▞▞[/]",
        subtitle=f"[bold {COLORS['warning']}]// Cyberpunk Recon Framework //[/]",
        border_style=Style(color=COLORS['secondary'], bold=True),
        padding=(1, 2)
    ))
    console.print(
        Align.center(
            f"[{COLORS['dim']}]─────────────────────────────────────────────[/]"
        )
    )
    console.print(
        Align.center(
            f"[bold {COLORS['success']}]◉ SYSTEM ONLINE[/]  "
            f"[{COLORS['dim']}]|[/]  "
            f"[bold {COLORS['warning']}]⚡ V1.0[/]  "
            f"[{COLORS['dim']}]|[/]  "
            f"[bold {COLORS['primary']}]✦ EyeXscan[/]"
        )
    )
    console.print()

# ==================== MAIN SCAN ====================
def scan_website(url):
    try:
        url = clean_url(url)
        domain = get_domain(url)

        with Progress(
            SpinnerColumn(style=COLORS['primary'], spinner_name="dots12"),
            TextColumn(f"[progress.description]{{task.description}}"),
            BarColumn(
                complete_style=COLORS['primary'],
                finished_style=COLORS['success'],
                pulse_style=COLORS['secondary']
            ),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            main_table = create_styled_table(f"WEBSITE SCAN RESULTS: {url}")
            scan_task = progress.add_task(
                f"[{COLORS['info']}]Initializing...",
                total=100
            )

            # --- IP & DNS ---
            progress.update(scan_task, advance=10,
                            description=f"[{COLORS['info']}]◉ Checking IP and DNS...")
            try:
                ip = socket.gethostbyname(domain)
                main_table.add_row("IP Address", f"[{COLORS['success']}]{ip}[/]")

                dns_records = dns.resolver.resolve(domain, 'A')
                dns_ips = [str(record) for record in dns_records]
                if dns_ips:
                    main_table.add_row("DNS Records", f"[{COLORS['accent']}]" + "\n".join(dns_ips) + "[/]")
            except Exception as e:
                main_table.add_row("Network Info", f"[{COLORS['error']}]Error: {str(e)}[/]")

            # --- SSL ---
            progress.update(scan_task, advance=20,
                            description=f"[{COLORS['info']}]◉ Checking SSL...")
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        main_table.add_row("SSL Valid From", f"[{COLORS['success']}]{format_date(cert['notBefore'])}[/]")
                        main_table.add_row("SSL Valid Until", f"[{COLORS['warning']}]{format_date(cert['notAfter'])}[/]")
            except Exception as e:
                main_table.add_row("SSL Status", f"[{COLORS['error']}]Error: {str(e)}[/]")

            # --- HTTP Headers ---
            progress.update(scan_task, advance=20,
                            description=f"[{COLORS['info']}]◉ Checking HTTP Headers...")
            try:
                response = requests.get(url, timeout=5)
                status_color = COLORS['success'] if response.status_code == 200 else COLORS['warning']
                main_table.add_row(
                    "HTTP Status",
                    f"[{status_color}]{response.status_code} ({response.reason})[/]"
                )

                security_headers = get_security_headers(response.headers)
                for header, value in security_headers.items():
                    if value == 'Not Available':
                        main_table.add_row(header, f"[{COLORS['error']}]{value}[/]")
                    else:
                        main_table.add_row(header, f"[{COLORS['success']}]{value}[/]")
            except Exception as e:
                main_table.add_row("HTTP Status", f"[{COLORS['error']}]Error: {str(e)}[/]")

            # --- WHOIS ---
            progress.update(scan_task, advance=20,
                            description=f"[{COLORS['info']}]◉ Fetching WHOIS Info...")
            try:
                domain_info = whois.whois(domain)
                if domain_info.creation_date:
                    creation_date = domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date
                    main_table.add_row("Domain Created", f"[{COLORS['accent']}]{format_date(creation_date)}[/]")
                if domain_info.expiration_date:
                    expiration_date = domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date
                    main_table.add_row("Domain Expiry", f"[{COLORS['warning']}]{format_date(expiration_date)}[/]")
            except Exception as e:
                main_table.add_row("WHOIS Info", f"[{COLORS['error']}]Error: {str(e)}[/]")

            # --- Admin Panel ---
            progress.update(scan_task, advance=10,
                            description=f"[{COLORS['info']}]◉ Checking Admin Panel...")
            admin_panels = check_admin_panel(url)
            if admin_panels:
                main_table.add_row(
                    "Admin Panel",
                    f"[{COLORS['warning']}]" + "\n".join(admin_panels) + "[/]"
                )
            else:
                main_table.add_row("Admin Panel", f"[{COLORS['dim']}]Not Found[/]")

            # --- Server Info ---
            progress.update(scan_task, advance=10,
                            description=f"[{COLORS['info']}]◉ Fetching Server Info...")
            server, x_powered_by = grab_banner(url)
            main_table.add_row("Server", f"[{COLORS['secondary']}]{server}[/]")
            main_table.add_row("X-Powered-By", f"[{COLORS['secondary']}]{x_powered_by}[/]")

            # --- Technologies ---
            progress.update(scan_task, advance=10,
                            description=f"[{COLORS['info']}]◉ Detecting Technologies...")
            technologies = get_technologies(url)
            main_table.add_row("Technologies", f"[{COLORS['dim']}]{technologies}[/]")

            # --- Server Location ---
            progress.update(scan_task, advance=10,
                            description=f"[{COLORS['info']}]◉ Locating Server...")
            city, country = get_server_location(url)
            main_table.add_row("Server Location", f"[{COLORS['accent']}]{city}, {country}[/]")

            progress.update(scan_task, completed=100,
                            description=f"[{COLORS['success']}]✔ Scan Complete!")
            time.sleep(0.5)

        console.print()
        console.print(main_table)
        console.print(
            Align.center(
                f"[bold {COLORS['success']}]◤ SCAN FINISHED ◢[/]"
            )
        )
        console.print()

    except Exception as e:
        console.print(Panel(
            f"[bold {COLORS['error']}]✖ SCAN ERROR:[/] {str(e)}",
            border_style=Style(color=COLORS['error'], bold=True),
            title=f"[{COLORS['error']}]SYSTEM FAILURE[/]"
        ))

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    show_banner()

    try:
        url_input = console.input(
            f"[bold {COLORS['primary']}]┌─[[/]"
            f"[bold {COLORS['secondary']}]EyeXscan[/]"
            f"[bold {COLORS['primary']}]@[/]"
            f"[bold {COLORS['success']}]cyberpunk[/]"
            f"[bold {COLORS['primary']}]]─[[/]"
            f"[bold {COLORS['warning']}]Masukkan URL[/]"
            f"[bold {COLORS['primary']}]]\n"
            f"└──▶ [/]"
        ).strip()

        if not url_input:
            console.print(Panel(
                f"[bold {COLORS['error']}]✖ URL tidak boleh kosong![/]",
                border_style=Style(color=COLORS['error'])
            ))
        else:
            console.print()
            console.print(
                f"[{COLORS['dim']}]» Target: [{COLORS['primary']}]{url_input}[/][/{COLORS['dim']}]"
            )
            console.print()
            scan_website(url_input)

    except KeyboardInterrupt:
        console.print()
        console.print(Panel(
            f"[bold {COLORS['warning']}]⚠ Scan dibatalkan oleh user.[/]",
            border_style=Style(color=COLORS['warning']),
            title=f"[{COLORS['warning']}]ABORTED[/]"
        ))
    except Exception as e:
        console.print(Panel(
            f"[bold {COLORS['error']}]✖ Error:[/] {str(e)}",
            border_style=Style(color=COLORS['error'])
        ))