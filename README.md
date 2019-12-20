Postaram się tutaj wyjaśnić co bardziej nie zrozumiałem lub po prostu zawile zrobione
funkcje/funkcjonalności albo jakieś dziwne relacje pomiędzy obiektami

Kolory są przedstawione jako liczby
1 - niebieski
2 - zielony
3 - żółty
4 - czerwone

Poszczególne pola na których mogą znaleźć się pionki są zapisane w tablicach jednowymiarowych jako
trójki (x, y, color), gdzie x, y to współrzędne natomiast color określa jaki kolor znajduje się
aktualnie na danym polu.
Tablica nie jest podzielona na tuple ani inne tablice tylko jest ciągiem liczb dlatego wzory są
ociupine bardziej skomplikowane.

fieldPosArr -> tablica pozycji po których mogą poruszać się wszystkie piony
homePosArr -> tablica pozycji startowych(home), wszystkie 4 kolory mają pozycje startowe w tej samej
    tablicy w kolejności (indeksów):
    0, 3 -> niebieskie
    4, 7 -> zielone
    8, 11 -> żółte
    12, 15 -> czerwone
endingPosArr -> tablica pozycji końcowych(castle), nie można ich stąd już przemieścić, jeżeli chodzi o
    kolory to historia ta sama co z tablicą homePosArr


Board:
render(): wywołuje tylko render, "animacją" pionów zajmują się już same piony


Pawn:
(dislaimer: nie wiem jak się robi silniki gier więc jest tutaj interpolacja dla animacji
    "werjsa bieda")
render(): poza renderem występuje przesunięcie o wyliczony wczęsniej w moveParams() krok

throwIntoGame(): po naciśnieciu na pion znajdujący się w domu "home" ustawia mu parametry
    (moveParams()) animacji oraz cel

move(): jeżli pion zrobi okrążenie wrzuca go do zamku(pozycja końcowa), uruchamia funkcję zbijania
    pionów w board lub tylko ustawia parametry ruchu

moveParams(): funkcja odpowiedzialna za "animacje" pionów


gameCube:
