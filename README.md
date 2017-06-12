# fluffy-spork
_Posortować ponad 1000 zdjęć_
___
## Cel
Posortować około 1000 zdjęć dokumentów o różnej jakości.
Dokumenty traktują o zakresach czynności pracowników.

### Baza Danych
Nierelacyjna lub JSON
* Każde _raw_ zdjęcie posiada własny wpis w kolekcji dokumentów
* Każdy element posiada swoje ID oraz lokalizacje oryginalnego pliku.
* Element może posiadać lokalizacje przetworzonych plików.
* Element może posiadać __numer identyfikacyjny__
* Element może posiadać __stanowisko pracy__
* Element może posiadać __macierzystą komórkę organizacyjną__  

__Pogrubione atrybuty__ mogą pojawić się kilka razy ponieważ mogą pochodzić z różnych źródeł.
