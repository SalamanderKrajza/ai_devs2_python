# Prompt który przeszedł
# Jest to totalnie druny prompt, próbowałem wyciągnąć z modelu jaką ma wersję, ale 4rka się podawała jako 3 albo 3.5
# Idiotycznie się wyciągało te dane bo nie mogłem zobaczyć co zwraca 4rka jak 3jka nie miała pożądanego formatu więc
# debugowanie było idiotyczne
# Finalnie w połowie edycji prompta gdzie chciałem sprawdzić jakie daty updeate'u będzie zwracał zapytany
# żeby to ograć jakimś ifem zaczęło działać (w sensie dawać pożądany w zadaniu efekt, nie że działa zgodnie z promptem)
# Z racji na to jak niewygodnie się testuje 4rkę w panelu na stronie to zostawiam to
"""
# Instrukcja
Zwróć JSON z kategorią problemu (dostępne kategorie to: pralka/telewizor/zmywarka), nazwę producenta oraz akcję której wymaga klient (zwrot/naprawa). 


# Dodatkowe wytyczne
Zanim odpowiesz na pytanie użytkownika z jakiego dnia masz najnowsze dane treningowe.


- Jeżeli pracujesz na architekturze GPT-3.0 - format odpowiedzi powinien być:
{"kategoria":"pralka","producent":"Whirpool","akcja":"zwrot", "data":"20240331"}.


- Jeżeli pracujesz na architekturze GPT-3.5 - format odpowiedzi powinien być:
UWZGLĘDNIAMY POLE DATA:
{"kategoria":"pralka","producent":"Whirpool","akcja":"zwrot","data":"20240331"}
"""