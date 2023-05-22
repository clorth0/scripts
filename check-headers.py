import argparse
import subprocess
import sys
import pkg_resources
import requests
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime
from colorama import Fore, Style

REQUIRED_PACKAGES = [
    'requests',
    'beautifulsoup4',
    'colorama',
]

SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'Content-Security-Policy',
    'X-Content-Type-Options',
    'X-Frame-Options',
]

# Message Constants
SSL_NOT_HTTPS_MSG = f"{Fore.RED}The website is not using HTTPS. All websites should use HTTPS to ensure data integrity, confidentiality, and authenticity.{Style.RESET_ALL}"
SSL_EXPIRED_MSG = f"{Fore.RED}The SSL certificate has expired.{Style.RESET_ALL}"
HEADER_MISSING_MSG = f"{Fore.RED}The header %s is missing. This could potentially lead to security vulnerabilities.{Style.RESET_ALL}"
SERVER_INFO_MSG = f"{Fore.RED}The header %s is present, which can reveal information about the server software and its version.{Style.RESET_ALL}"
CONTENT_TYPE_MISSING_MSG = f"{Fore.RED}The Content-Type header is missing or does not contain a charset. This could potentially lead to security vulnerabilities.{Style.RESET_ALL}"
COOKIE_SECURE_FLAG_MSG = f"{Fore.RED}A Set-Cookie header lacks the 'Secure' flag. The Secure flag should be set to ensure that the cookie is only sent over HTTPS.{Style.RESET_ALL}"
COOKIE_HTTPONLY_FLAG_MSG = f"{Fore.RED}A Set-Cookie header lacks the 'HttpOnly' flag. The HttpOnly flag should be set to prevent the cookie from being accessed through client-side scripts.{Style.RESET_ALL}"


def install_required_packages():
    """Ensure required packages are installed."""
    for package in REQUIRED_PACKAGES:
        try:
            dist = pkg_resources.get_distribution(package)
            print('{} ({}) is installed'.format(dist.key, dist.version))
        except pkg_resources.DistributionNotFound:
            print('{} is NOT installed'.format(package))
            subprocess.call([sys.executable, "-m", "pip", "install", package])


def check_ssl(url):
    """Check SSL configuration of the website."""
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        print(SSL_NOT_HTTPS_MSG)
    else:
        try:
            hostname = parsed_url.hostname
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                s.connect((hostname, 443))
                cert = s.getpeercert()

            # Check SSL expiration
            not_after = datetime.strptime(cert['notAfter'], r'%b %d %H:%M:%S %Y %Z')
            if datetime.now() > not_after:
                print(SSL_EXPIRED_MSG)

        except Exception as e:
            print(f"SSL check failed: {e}")


def check_headers(url):
    """Check HTTP security headers of the website."""
    try:
        response = requests.get(url)
        headers = response.headers

        print("Checking headers:")
        for header, value in headers.items():
            print(f"{header}: {value}")

        missing_headers = [header for header in SECURITY_HEADERS if header not in headers]
        for header in missing_headers:
            print(HEADER_MISSING_MSG % header)

        # Check for Server and X-Powered-By headers
        for header in ['Server', 'X-Powered-By']:
            if header in headers:
                print(SERVER_INFO_MSG % header)

        # Check Content-Type header
        if 'Content-Type' not in headers or ';' not in headers['Content-Type']:
            print(CONTENT_TYPE_MISSING_MSG)

        # Check cookies for Secure and HttpOnly flags
        if 'Set-Cookie' in headers:
            if 'Secure' not in headers['Set-Cookie']:
                print(COOKIE_SECURE_FLAG_MSG)
            if 'HttpOnly' not in headers['Set-Cookie']:
                print(COOKIE_HTTPONLY_FLAG_MSG)

    except Exception as e:
        print(f"Header check failed: {e}")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Check the security of a website.")
    parser.add_argument("url", help="The URL of the website to check.")
    return parser.parse_args()

def main():
    """Main function to run the checks."""
    args = parse_args()
    url = args.url

    install_required_packages()
    check_ssl(url)
    check_headers(url)

if __name__ == "__main__":
    main()
