# Summary of the document Lekcja kursu AI_Devs, S03L03 — Wyszukiwanie i bazy wektorowe

### Rozdział 3, Lekcja 3 - Wyszukiwanie i bazy wektorowe 

Długoterminowa pamięć dla modelu jest jednym z najbardziej użytecznych zastosowań LLM (Long-term Language Model), ze względu na możliwość **hiper-personalizacji** doświadczeń oraz **zbudowania częściowo autonomicznych zachowań**. To otwiera drzwi do niespotykanych wcześniej zastosowań.

Bazy wektorowe to miejsce, gdzie przechowujemy i przeszukujemy wyniki tokenizacji oraz embeddingu, które omówiliśmy w lekcji **C01L02**. Poniżej znajduje się **uproszczona wizualizacja** wielowymiarowych danych, przedstawionych w przestrzeni 3D. Wizualizację tę można zobaczyć [tutaj](https://projector.tensorflow.org).

![](https://cloud.overment.com/word2vec-1695711060.gif)

### Porównywanie wektorów i cosine similarity 

Wektory można porównywać, aby określić **podobieństwo** między nimi, co umożliwia odnalezienie zbliżonych danych. Techniką często stosowaną w tym celu jest **cosine similarity**. Metoda ta daje nam wartość od -1 do 1, gdzie -1 oznacza semantyczne odwrotności, 0 oznacza brak semantycznego powiązania, a 1 oznacza semantyczne powiązanie. 

Przykładowo, na obrazku poniżej słowo **komputer** zostało powiązane ze **sprzęt, oprogramowanie, programowanie, pc, grafika, IBM czy Macintosh** dzięki zastosowaniu cosine similarity. 

![](https://cloud.overment.com/cosine-cc650e6b-1.png)

Bazy wektorowe mogą przeprowadzać obliczenia za nas i zwrócić wyniki z "similarity score". Na podstawie tych wyników możemy wybrać tylko te wpisy, które są najbardziej zbliżone znaczeniem do zapytania.

### Jak dodawać dane do indeksu bazy wektorowej 

Dodawanie danych do indeksu bazy wektorowej to proces, który obejmuje:

1. Przygotowanie **dokumentu** w postaci **treści oraz metadanych**
2. Wygenerowanie embeddingu, np. za pomocą text-embedding-ada-002
3. Zapisanie embeddingu w bazie **w połączeniu z metadanymi**

Zarządzanie bazami danych na podstawowym poziomie może sprowadzać się do **prostej interakcji przez API** i zapytań CRUD. Niemniej jednak, budowanie dynamicznego kontekstu dla LLM może być bardziej skomplikowane.

Odnajdywanie treści (nie tylko tekstu) o podobnym znaczeniu jest istotnym elementem budowania dynamicznego kontekstu dla LLM.

W dalszych lekcjach będziemy omawiać szczegóły pracy z bazami wektorowymi, w tym podejście no-code. Na razie warto zwrócić uwagę na kilka aspektów:

- Zwróć uwagę na to, jak opisywanie danych wspomaga proces wyszukiwania. Możesz to zobaczyć na przykładzie **11_docs**, gdzie pokazałem, jak generować dokumenty i opisywać je za pomocą metadanych.

- W kodzie zwróć uwagę na użycie metody **similaritySearchWithScore**. Drugi argument tej metody to liczba rekordów, które chcemy otrzymać (tzw. topK). Zwiększając tę wartość, dostaniemy więcej rekordów, które możemy potem dodatkowo filtrować lub grupować używając metadanych.

- Filtrowanie może odbyć się już na etapie wyszukiwania, dzięki możliwości przekazania obiektu określającego dopasowania metadanych, które chcemy brać pod uwagę.

- Ważne jest też, by zrozumieć, że **Similarity Search i bazy wektorowe nie są odpowiedzią na wszystkie pytania**. Są bardzo użyteczne na etapie prototypu, ale budowanie czegoś więcej niż tylko demo wymaga więcej narzędzi i podejść.

![](https://cloud.overment.com/search-66da96ba-1.png)

Przykład pokazuje użycie małej bazy wiedzy jako długiego dokumentu z informacjami na temat osoby. Używając bazy wektorowej do wyszukania fragmentów powiązanych semantycznie z zapytaniem: "Czym zajmuje się Adam?", dokumenty pierwszy i trzeci są identyfikowane jako istotne. Więcej na ten temat można dowiedzieć się z przykładu **22_simple**. Ważne jest jednak, aby unikać mieszania języków - jeśli baza wiedzy jest tworzona w jednym języku, zapytania powinny być kierowane w tym samym języku. 

Jednak w praktyce często zdarza się, że interesująca informacja jest rozbita na więcej niż jeden fragment. Na przykład, opis specjalizacji może być rozdzielony między różne dokumenty, co może prowadzić do pominięcia niektórych istotnych informacji podczas wyszukiwania. 

![Przykład wyszukiwania semantycznego](https://cloud.overment.com/chunks-2033514e-7.png)

![Wyszukiwanie z użyciem vector store](https://cloud.overment.com/simple-2adcdec1-f.png)

![Przykład pominięcia informacji](https://cloud.overment.com/miss-12acc7c6-f.png)

W przykładzie **23_fragmented** zwiększenie limitu wyszukiwania dokumentów (topK) na trzy pierwsze wyniki nie skutkuje odnalezieniem drugiego dokumentu. Jeśli na tej podstawie zbudujemy kontekst dla modelu, odpowiedzi udzielone przez niego będą niepełne. Taka sytuacja może prowadzić do utraty precyzji, co jest niepożądane. Istnieje również ryzyko, że niedokładne odnalezienie danych skończy się wstrzyknięciem do kontekstu informacji, które doprowadzą do halucynacji modelu, czyniąc system bezużytecznym lub nawet szkodliwym. ![](https://cloud.overment.com/fragmented-500ae0cc-c.png)

Rozwiązanie tego problemu jest tematem dłuższych lekcji. 

W lekcji **1.5** poruszono temat organizacji oraz dostosowania danych, który teraz przeniesiemy na bardziej dosłowny wymiar.

W tym fragmencie omówiliśmy wyzwanie pracy z różnymi formatami nieustrukturyzowanymi danych. Przykładem jest kod **24_files**, który jest rozszerzeniem wcześniejszego kodu **12_web**. Chociaż każdy format pliku ma swoje unikalne wyzwania, skupiamy się na uniwersalnych koncepcjach. Celem jest stworzenie zestawu danych na podstawie informacji o nas, twórcach AI_Devs, bezpośrednio ze strony aidevs.pl. Pierwszym krokiem jest zapisanie treści strony jako pliku HTML, który następnie wczytujemy do kodu. ![Zrzut ekranu z aidevs.pl](https://cloud.overment.com/instructors-6f5f8bbc-1.png)

Plik HTML zawiera mnóstwo szumu, takiego jak tagi HTML, style CSS czy skrypty JavaScript, co czyni go trudnym do zrozumienia dla modelu. Podobne wyzwania pojawiłyby się przy pracy z innymi formatami plików, poza plikami .txt czy plikami markdown. ![Zrzut ekranu z pliku HTML](https://cloud.overment.com/html-04554502-3.png)

Omówione zostało zadanie podziału dokumentu na mniejsze fragmenty, z uwzględnieniem metadanych. Przykładem była potrzeba podzielenia tekstu na sekcje dotyczące trzech autorów. W tym celu użyto nagłówków H3 (oznaczonych w Markdown jako '###'), jednakże zauważono, że nagłówki w strukturze HTML znajdują się **poniżej zdjęć**. Stąd konieczność uwzględnienia zdjęć w podziale. Wskazano, że błędne zastosowanie podziału według znaków '###' powoduje, że link do zdjęcia autora znajduje się poza sekcją go opisującą (![](https://cloud.overment.com/split-cc2d40ca-5.jpg)). Aby osiągnąć prawidłowy podział, zastosowano wyrażenie regularne, które rozwiązało ten problem. Wiedza na temat wyrażeń regularnych okazała się przydatna, a do stworzenia odpowiedniego wyrażenia wykorzystano model GPT-4.

### CXXLXX - Opis dokumentów i przetwarzanie długich tekstów

Podczas pracy z dokumentami, warto zwrócić uwagę na metadane, które mogą znacznie ułatwić nam pracę. Używając wyrażeń regularnych, możemy automatycznie pobierać takie informacje jak imiona autorów. Dodatkowo, niektóre metadane możemy wpisywać ręcznie, jeśli nie są one generowane dynamicznie. 

Linki znajdujące się w treści dokumentu mogą zużywać dużo tokenów, dlatego warto przenieść je do metadanych. W treści dokumentu zamiast linków, możemy umieścić indeksy poprzedzone dolarem. W ten sposób, na późniejszym etapie, będziemy mogli łatwo je podmienić. 

![](https://cloud.overment.com/described-17bfed2b-2.png)

Tak przygotowane dokumenty są gotowe do indeksowania w bazie wektorowej i wykorzystania w dynamicznym kontekście. 

![](https://cloud.overment.com/docs-82a00d0c-1.png)

Różnica między oryginalnymi danymi a tak przetworzonymi dokumentami jest ogromna i z pewnością wpływa na efektywność systemu. Na podstawie zdobytej wiedzy, możemy stworzyć prostego czatbota, odpowiadającego na pytania na temat twórców AI_Devs.


### Praca z dużymi danymi w LLM 

Podczas pracy z danymi podłączanymi do LLM, zwykle napotykamy na sytuacje, gdzie potrzebnych informacji jest więcej, niż możemy zmieścić w kontekście. Przyjrzyjmy się kilku z nich: 

- **Przetwarzanie** długiego dokumentu, np. na potrzeby korekty czy tłumaczenia. 
- **Klasyfikacja** dużych zestawów danych, np. za pomocą tagów, kategorii czy etykiet. 
- **Wzbogacanie** danych na potrzeby użytkownika lub systemu (np. wyszukiwania czy rekomendacji). 
- **Kompresja** obszernych treści, np. poprzez podsumowanie, co może być użyteczne zarówno dla użytkownika, jak i systemu. 
- **Interakcja** z danymi w formie czatbota lub w celu pozyskiwania zewnętrznych informacji na potrzeby realizowanego zadania. 

Aby zobrazować te koncepcje, przygotowaliśmy prosty scenariusz przy użyciu platformy make.com. Możesz go wykorzystać w połączeniu ze swoim kodem lub odwzorować jego mechanikę za pomocą kodu. 

![](https://cloud.overment.com/processing-f7af380e-4.png) 

> UWAGA: Przy testowaniu tego scenariusza, zalecamy korzystanie z krótkich plików. Przetwarzanie długich treści za pomocą modelu GPT-4 może generować znaczne koszty. 

⚡ [Pobierz Blueprint Scenariusza](https://cloud.overment.com/aidevs_process_file-1695994995.json)

## Rozdział 3, Lekcja 2

### Elastyczność zadań badawczych

Scenariusz badawczy jest **izolowanym zadaniem**, które można wywołać na różne sposoby. Możliwe jest wywołanie na żądanie (np. podczas rozmowy z AI), według harmonogramu (np. o ustalonej porze) lub na skutek określonego zdarzenia (np. dodania pliku do Google Drive). Taka elastyczność zwiększa użyteczność tego typu zadań.

Dodatkowo, do zadania można przekazać dodatkowe informacje, które **nadają kontekst** lub modyfikują instrukcję systemową, co jeszcze bardziej zwiększa użyteczność rozwiązania.

### Zastosowanie w tłumaczeniach

Scenariusz o podobnej strukturze został już wielokrotnie wykorzystany do tłumaczeń treści o długości około 25 000 znaków. Przy dłuższych formach, takich jak książki, warto rozważyć zastosowanie tego samego schematu w formie kodu. Daje to większą kontrolę nad ewentualnymi błędami i pozwala na oszczędność wynikającą z liczby wykonanych operacji, za które rozlicza make.com.


### Automatyczne przetwarzanie pliku

Podczas przetwarzania pliku automatycznie, ważne jest, aby model był świadomy, że ma do czynienia z **fragmentami** dłuższego dokumentu. Ze względu na prostą logikę podziału treści, fragmentem może być nawet jedno zdanie, dlatego warto dodać **dodatkowy kontekst** np. poprzez przekazanie nazwy pliku lub innych pomocnych informacji. To pozwoli na lepsze dopasowanie tłumaczenia, szczególnie w przypadku słów i wyrażeń o różnych znaczeniach. 

![Kontekst](https://cloud.overment.com/prompt-e7738b20-3.png)

Możliwe jest przetestowanie działania scenariusza za pomocą CURL'a lub zapytania HTTP w dowolnej innej formie. Pamiętaj o podmianie nazwy pliku i adresu webhooka powiązanego ze scenariuszem. 

![Test](https://cloud.overment.com/curl-2d752ffc-b.png)

Scenariusz przetwarzający pliki można uruchamiać na różne sposoby. Można na przykład utworzyć **inny katalog na Google Drive, np. 'Do przetłumaczenia'** i 'obserwować' go za pomocą scenariusza make.com lub uruchamiać go np. raz dziennie. Jest to przykład korzyści wynikających z 'izolowania' scenariuszy realizujących konkretne zadania. 

![Przetwarzanie](https://cloud.overment.com/process-e7445b93-a.png)

- ⚡ [Pobierz blueprint](https://cloud.overment.com/aidevs_watch_folder-1695994706.json)

