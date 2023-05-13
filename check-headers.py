import requests

def check_vulnerable_headers(url):
    response = requests.get(url)
    headers = response.headers

    print("Checking for vulnerable headers...")
    if "X-Frame-Options" not in headers:
        print("\033[91m[X] Missing X-Frame-Options header: This may expose your website to clickjacking attacks.\033[0m")
    if "Content-Security-Policy" not in headers:
        print("\033[91m[X] Missing Content-Security-Policy header: This may leave your website vulnerable to cross-site scripting (XSS) attacks.\033[0m")
    if "Strict-Transport-Security" not in headers:
        print("\033[91m[X] Missing Strict-Transport-Security header: This may make your website susceptible to SSL-stripping attacks.\033[0m")

def check_ssl_issues(url):
    response = requests.get(url, verify=True)
    if response.status_code == 200:
        print("Checking for SSL issues...")
        if not response.url.startswith("https://"):
            print("\033[91m[X] Insecure SSL connection: Your website is not using a secure (HTTPS) connection.\033[0m")
        elif response.history and not response.history[0].url.startswith("https://"):
            print("\033[91m[X] Insecure SSL redirect: Your website is redirecting to an insecure (HTTP) page.\033[0m")

def check_website_security(url):
    print("Checking website security for:", url)
    check_vulnerable_headers(url)
    check_ssl_issues(url)

# Example usage
check_website_security("https://example.com")
