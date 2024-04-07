# Summary of the document Lekcja kursu AI_Devs, S03L03 — Wyszukiwanie i bazy wektorowe

#### S03L03 — Wyszukiwanie i bazy wektorowe

Długoterminowa pamięć dla modelu to jedno z najbardziej użytecznych zastosowań LLM. Z jednej strony, pozwala na **hiper-personalizację** doświadczeń, a z drugiej na **zbudowanie częściowo autonomicznych zachowań**. 

## Czym są bazy wektorowe?

To miejsce, gdzie przechowujemy i przeszukujemy wyniki tokenizacji oraz embeddingu, o których mówiliśmy w lekcji **C01L02**. [Tutaj](https://projector.tensorflow.org) możesz zobaczyć **uproszczoną wizualizację** wielowymiarowych danych w przestrzeni 3D.

![](https://cloud.overment.com/word2vec-1695711060.gif)

Bazy wektorowe umożliwiają porównywanie wektorów, dzięki czemu możemy określić **podobieństwo** między nimi. Wykorzystując metodę **cosine similarity**, otrzymujemy wartość od -1 do 1, która pokazuje, jak bardzo dane są semantycznie powiązane. Na podstawie tych wyników możemy wybrać dane, które są najbardziej zbliżone do naszego zapytania. Na obrazku poniżej widać, jak słowo **komputer** zostało powiązane ze **sprzęt, oprogramowanie, programowanie, pc, grafika, IBM czy Macintosh**.

![](https://cloud.overment.com/cosine-cc650e6b-1.png)

### Rozmowa z własną bazą wiedzy

W najprostszym scenariuszu chcemy generować małe dokumenty, które zawierają informacje istotne dla modelu, ale nie zaburzają ich kontekstu. Czyli chcemy mieć dokumenty jak najkrótsze, ale jednocześnie zrozumiałe.

Przykładowo, mając bazę wiedzy zawierającą informacje na mój temat, moglibyśmy użyć bazy wektorowej do wyszukania fragmentów powiązanych semantycznie z zapytaniem: "Czym zajmuje się Adam?". Na przykładzie [**22_simple**](https://cloud.overment.com/22_simple) widać, jak wykorzystujemy prosty vector store do przechowania dokumentów w pamięci i wyszukiwania ich poprzez similarity search.

![](https://cloud.overment.com/chunks-2033514e-7.png)

![](https://cloud.overment.com/simple-2adcdec1-f.png)

Ważne jest, aby unikać mieszania języków. Jeżeli bazę wiedzy budujesz po angielsku, to stosuj ten język także w przypadku kierowanej do niej zapytań.

Jednakże, w praktyce często spotykamy scenariusz, w którym interesująca nas informacja została rozbita na więcej niż jeden fragment. Na przykład, opis mojej specjalizacji znajduje się w pierwszym, drugim i czwartym dokumencie, ale informacja z pierwszego fragmentu jest kontynuowana w drugim, który nie został wskazany jako istotny.

![](https://cloud.overment.com/miss-12acc7c6-f.png)

## CXXLXX Konwersja HTML do Markdown

Zrozumienie oryginalnego pliku HTML przez model może być utrudnione przez obecność szumu w postaci tagów HTML, stylów CSS czy skryptów JavaScript. Ten problem występuje również w przypadku wielu innych formatów plików, z wyjątkiem prostych formatów tekstowych jak .txt czy markdown.

Przykładem może być strona [aidevs.pl](https://aidevs.pl), która jest dość obszerna. Jeśli interesuje nas tylko jedna sekcja, dobrym podejściem jest usunięcie wszystkiego poza nią. Można to zrobić za pomocą narzędzia do parsowania dokumentów HTML, jak na przykład [cheerio](https://www.npmjs.com/package/cheerio). Wykorzystując go, można pobrać treść konkretnego tagu, w tym przypadku diva z identyfikatorem **instructors**.

![](https://cloud.overment.com/authors-300c2ea4-c.png)

Po takim zabiegu nasze dane wciąż zawierają wiele niepotrzebnych elementów. Można je zamienić na zwykły tekst, ale trzeba pamiętać o docelowym zastosowaniu - kontekście dla modelu języka. Ważne jest nie tylko zawartość tekstowa, ale także formatowanie, linki i obrazy, a w przypadku większych zbiorów danych - źródła jako referencje.

Najprostszym sposobem na przekonwertowanie HTML na format przyjazny dla modelu jest zamiana go na składnię Markdown. Do tego celu można wykorzystać narzędzia jak [node-html-markdown](https://www.npmjs.com/package/node-html-markdown).

![](https://cloud.overment.com/markdown-ac61f421-6.png)

Ostatecznie, dążymy do stworzenia dokumentów opisanych metadanymi. W tym celu, nasz tekst powinien zostać podzielony na mniejsze fragmenty. Jeśli na przykład chcemy uzyskać informacje o trzech autorach, możemy podzielić treść na fragmenty opisujące każdego z nich.

