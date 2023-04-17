# Śledzenie obiektu kolorowego (czerwona piłka)

Napisz program, którego zadaniem jest śledzenie kolorowego obiektu (czerwona piłka).  Na filmie  movingball.mp4  jest poruszający się obiekt. Należy określić zakres kolorów czerwonej piłki. Dla każdej klatki filmu należy:

1. Zmienić format obrazu na HSV
2. Określić piksele, które spełniają wymagania koloru (czerwony obiekt)
3. Zastosować operacje morfologiczne celem poprawy maski (usunięcie szumów oraz wypełnienie braków)
4. Określić środek ciężkości piłki - współrzędne jej środka
5. Zaznaczyć na filmie środek ciężkości