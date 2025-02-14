projekt_03
Web Scraper

Jedná se o program, jenž scrapuje volební data z webu Volby.cz, a to konkrétné z url odkazu: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103. zde se nachází volební výsledky pro územní celek Prostějov
Nejprve si musíme vytvořit vlastní virtuální prostředí zadáním příkazu budo terminálu IDE nebo do příkazového řádku.
Příkaz vypadá následovně: python -m venv virtualni_prostredi
 Aktivace virtualního prostředí pro systém windows vypadá takto: virtualni_prostredi\Scripts\Activate.ps1
 Je třeba zkontrolovat, zda je prostředí je prostředí aktivní, abychom mohli pracovat na projektu:$ source moje_prvni_prostredi/bin/activate 
 Na začátku řádku se poté objeví jméno projektu v kulatých závorkách: (moje_prvni_prostredi) $
Dále potřebujeme do svého prostředí instolvat knihony třetích stran.
Jedná se o knihovnu bs4 a requests
příkazy píšeme do terminálu.
pip install bs4
pip install requests
Po napsání kódu jej spuštíme přes terminál takto: python projekt_03.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'prostejov.csv'
První argument je url odkaz:https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Druhý argument je název souboru csv: prostejov csv.
Pří správném spuštění program vypíše do csv souboru volení výsledky z daného odkazu.
Pokud uživatel nezadá oba argumenty (ať už nesprávné pořadí, nebo argument, který neobsahuje správný odkaz), program jej upozorní a nepokračuje.
