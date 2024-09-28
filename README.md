# PROJECT TITLE
DontBeAped

# Team Name
Apes together strong

# Team Memebers
Michal Switala, Jakub Switala, Maciej Switala

# Project Description

DontBeAped is designed to protect users from fake online store websites. The program's purpose is to ensure payment security by verifying the store's website at the moment the user is redirected to it. Some payment methods (like card payments) have mechanisms for disputes/chargebacks, while others do not. Any payment deemed less secure will trigger a store data check, and in the case of unreliability, an appropriate alert will be raised.
Additionally, the program compares the price of the product offered in the store with competitors, and if the price is suspiciously low, an alert will also be triggered.


# informacja dla mnie (kuba)

### niestety zeby zainstalowac te rzeczy na macos, musze utworzyc wirtualne srodowisko

utworz wirtualne srodowisko
```python3 -m venv venv```
aktywuj wirtualne srodowisko
```source venv/bin/activate```
zainstaluj potrzebne rzeczy:
```pip install requests beautifulsoup4```
```pip install scapy --index-url=https://pypi.python.org/simple```