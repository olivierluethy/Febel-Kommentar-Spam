/*
wie lässt sich mittels javascript für dev tools ein post request durchführen?
*/

fetch("https://febel.ch/ass/edit.php", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    name: "Max",
    value: 42
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

/*

[[Prototype]]: Promise[[PromiseState]]: "fulfilled"[[PromiseResult]]: undefined
VM697:13 SyntaxError: Unexpected token '<', "<br />
<b>"... is not valid JSON

Der Fehler sagt dir im Grunde zwei Dinge:

---

# ❌ **1. Der Server liefert kein JSON zurück**

Die Fehlermeldung:

```
SyntaxError: Unexpected token '<' ... is not valid JSON
```

bedeutet fast immer:

➡️ **Der Server gibt HTML zurück**, kein JSON.
Das `<` ist der Anfang eines HTML-Dokuments (z. B. eine Fehlermeldung oder Login-Seite).

Darum scheitert:

```js
response.json()
```

---

# ❌ **2. Der Server akzeptiert vermutlich auch kein JSON als Input**

Du sendest:

```js
Content-Type: application/json
body: JSON.stringify(...)
```

ABER die Datei **edit.php** erwartet ziemlich sicher kein JSON, sondern klassisches **POST-Formular (`application/x-www-form-urlencoded`)** oder **`multipart/form-data`**.

---

# ✅ **So machst du es richtig (wahrscheinlich): Form-POST statt JSON**

Versuche dieses Snippet:

```js
fetch("https://febel.ch/ass/edit.php", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: new URLSearchParams({
    name: "Max",
    value: 42
  })
})
  .then(r => r.text()) // <-- weil der Server HTML zurückgibt
  .then(console.log)
  .catch(console.error);
```

### Warum?

* Webseiten mit `.php` erwarten i.d.R. Formulardaten.
* Die Antwort ist **HTML**, also musst du `.text()` statt `.json()` verwenden.

---

# 🔍 **Optional: Automatisch anzeigen, was wirklich zurückkommt**

Wenn du wissen willst, was der Server wirklich liefert:

```js
fetch("https://febel.ch/ass/edit.php", {
  method: "POST",
  body: new URLSearchParams({ name: "Max" })
})
  .then(r => r.text())
  .then(html => {
    console.log(html);
  });
```

Damit siehst du die vollständige HTML-Antwort.

---

# ❗ Wichtiger Hinweis: CORS

Wenn dein Browser meldet:

```
Access-Control-Allow-Origin missing
```

…dann kannst du **aus dem Browser** nicht auf diese URL posten — außer du befindest dich direkt auf der Domain oder verwendest einen Proxy.

---

## Wenn du willst, kann ich dir auch sagen:

✔ wie man CORS umgeht (nur lokal!)
✔ wie man herausfindet, welche POST-Felder der PHP-Server erwartet
✔ wie man Request so baut wie ein echtes HTML-Formular

Sag einfach Bescheid!
