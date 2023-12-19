import requests
from bs4 import BeautifulSoup
import time
from twilio.rest import Client

# Twilio credentials and setup
account_sid = 'ENTER'
auth_token = 'ENTER'
twilio_client = Client(account_sid, auth_token)
twilio_phone_number = 'ENTER'
your_phone_number = 'ENTER'

def get_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def send_sms(message):
    message = twilio_client.messages.create(
        from_=twilio_phone_number,
        body=message,
        to=your_phone_number
    )
    print(f"Message sent: {message.sid}")

def main():
    url = 'https://www.tesla.com/en_US/teslaaccount/order/RN11286NNNN'
    initial_content = get_page_content(url)

    while True:
        time.sleep(3600) # 1 hour
        current_content = get_page_content(url)

        if current_content != initial_content:
            send_sms("Web page has changed!")
            initial_content = current_content

if __name__ == "__main__":
    main()
