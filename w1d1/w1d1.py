"""
Order asc ONLY FRUITS in format:
["A","C","Z"]
"""

"""
## Podejście 1
Spraw, aby ChatGPT poprawił poniższy kod tak, aby poprawnie zwracał zadaną liczbę ciągu Fibonnacciego. Kod jest napisany w PHP 8.1. Limit czasu wykonania funkcji to 2 sekundy. W przypadku jakichkolwiek błędów, zwracaną wartością z funkcji powinno być zero. Weź pod uwagę, że wyliczanie elementów ciągu Fibbonaciego jest BARDZO zasobożerne pod względem pamięci. Może warto pomyśleć o jakimś usprawnieniu? (GPT-4)

### Pierwszy wynik
function fib($n) {
    if ($n <= 0) {
        return 0;
    }
    $a = 0;
    $b = 1;
    for ($i = 2; $i <= $n; $i++) {
        $c = $a + $b;
        $a = $b;
        $b = $c;
    }
    return $b;
}

Test01 (małe liczby) = OK
Test02 (liczby ujemne) = OK
Test03 (tekst jako input) = 💀FATAL💀: PHP umarł (zjadłeś za dużo pamięci? 😋)NOK (przekroczono 2s)


W razie problemu z zadaniami, pamiętaj o naszej społeczności

### Podejście 2
Jak widzisz test 3 nie wyszedł, nie zoptymalizowałeś wystarczająco obsługi inputu jako tekstu
"""