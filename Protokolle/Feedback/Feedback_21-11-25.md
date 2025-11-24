# LobbyController

## Attribute

- player = ein einzelner Spieler? 
- lobby = eine einzelne Lobby
- qr = ein bestimmter QR-Code für eine bestimmte Lobby
- createdLobbies = aber hier eine ganze Liste von vielen Lobbys?

## Methoden

- createLobby: Hallo, wenn ich mal groß bin, werde ich ein Factory Method Pattern
- saveCurrentLobby: umständlicher Algorithmus, ineffizient; dafür gibt es Wörterbücher / Hashmaps; Refactoring: HTTP-Verarbeitung und Abspeichern im Wörterbuch trennen (nicht in derselben Funktion)
- getChosenLobbySettings: wieder ein umständlicher Algorithmus, Wörterbücher sind die Lösung
- getLobbyList: zwei verschiedene Rückgabeformate? Wieso [{}]? Das ist keine leere Liste
- ...
- checkInput und addWord: das hört sich nicht nach Methoden an, die zur Verwaltung der Lobby-Daten gehören, sondern eher in einen GameController passen

## generelle Hinweise
- Dictionaries ermöglichen schnelle Suche von Items
- es gibt eingebaute Methoden, um Listen zu durchsuchen
- einheitliche Rückgabe-Formate beachten
- Klassendiagramm und Sequenzdiagramm (Lobby erstellen, Lobby beitreten, neues Wort posten) fürs Refactoring der Software-Architektur vorbereiten
- fürs Refactoring: Design Patterns nutzen