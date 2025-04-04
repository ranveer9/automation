# the project monitors a specific product from the amazon website and if the product is below the specified target price then 
# an email is sent to the user about the dropped price.

import os
from dotenv import load_dotenv
import smtplib
import requests
from bs4 import BeautifulSoup

# loading email and passwords of the gmail
load_dotenv()

AMAZON_URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# the price below which an email is to be sent
target_price = 100

header = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

# requesting data from amazon about the product
response = requests.get(url=AMAZON_URL, headers=header)

# parsing HTML page
soup = BeautifulSoup(response.content, "html.parser")

# taking out the prices from the amazon website and joining the both strings and converting them to the float type.
integer_price = soup.select("span.a-price-whole")[0].get_text(strip=True)
decimal_price=soup.select("span.a-price-fraction")[0].get_text(strip=True)
total_price = float(integer_price+decimal_price)

# the name of the product
product_name = soup.select("#productTitle")[0].get_text(strip=True)

# if condition meets, then sending the email to the required address.
if total_price < target_price:
    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
        connection.sendmail(from_addr=os.environ["EMAIL_ADDRESS"],
                            to_addrs=os.environ["EMAIL_ADDRESS"],
                            msg=f"Subject: Amazon Price Alert!\n\n{product_name} is now ${total_price}.".encode("utf-8"))
    print("Chali gayi mail.....Check Karle")