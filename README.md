# Szoftverfejlesztési folyamatok projektmunka

## Hallgató adatai

- Név: Zimmermann Zsolt Gábor
- Neptun kód: IQMBGI
- h-s azonosító: h486510

## Választott alap projekt:

Aknakereső

## Megvalósítandó feature-ök

### IV. Megjelölési/Flagging rendszer

A játékosoknak lehetőséget kell biztosítani arra, hogy megjelöljék azokat a mezőket, ahol aknára gyanakodnak, így elkerülve a véletlen felfedést.

- Állapotbővítés: Bővítsük a mezők állapotát úgy, hogy különbséget tegyünk a "fedett", "felfedett" és "megjelölt" mezők között.
- Felhasználói bemenet: A játékos egy parancs segítségével (például "flag" és a koordináták megadásával) tudja beállítani vagy eltávolítani a megjelölést.
- Megjelenítés módosítása: A konzolon a megjelölt mezők egy egyedi szimbólummal (például "F") jelenjenek meg, hogy egyértelmű legyen a státuszuk.

### V. Utolsó lépés visszavonása

A játékosnak lehetőséget kell adni arra, hogy visszavonja az utolsó lépését, beleértve az összetettebb műveleteket (például a biztonságos területek automatikus felfedését - ha ezt megvalósítottuk).

- Lépésnaplózás: Minden lépést rögzítsünk (például egy verem vagy lista segítségével, vagy tetszőleges módon), beleértve a koordinátákat és a mezők korábbi állapotát.
- Visszavonási parancs: Implementáljunk egy "undo" parancsot, amely visszaállítja az utolsó lépés előtti állapotot.
- Kaszkádkezelés: Ha egy lépés több mezőt érintett (például a terjedési felfedés során), akkor minden érintett mezőt vissza kell állítani a mentett állapotnak megfelelően.
