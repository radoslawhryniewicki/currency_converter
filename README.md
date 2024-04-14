#### Autor: Radosław Hryniewicki

- `example_currency_rates.json` - lokalne źródło danych z kursami walut
- `database.json` - baza danych z zapisanymi kursami walut

Plik uruchamialny tj. skrypt służący do konwersji kwoty na podaną przez użytkownika walutę znajduje się w pliku script.py


Aby uruchomić skrypt dla środowiska testowego należy uruchomić komendę :
 > python script.py --env=dev


 Aby uruchomić skrypt dla środowiska produkcyjnego należy uruchomić komendę :
 > python script.py --env=prod


 Testy jednostkowe można uruchomić poleceniem:
 > pytest .

