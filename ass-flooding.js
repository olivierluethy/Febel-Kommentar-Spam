const titel = [
  "Du bisch en guete",
  "Legende aus",
  "King vom",
  "BischHammer",
  "Weltmeister",
  "GOAT",
  "Der Chef",
  "Absoluter Boss",
  "Unschlagbar",
  "Master of",
  "Kaiser von",
  "Godmode",
  "Pro Gamer",
  "Einzigartig",
  "Ultimativer"
];

async function spamFebel() {
  let counter = 0;

  while (true) {
    counter++;

    const randomTitel = titel[Math.floor(Math.random() * titel.length)];
    const uniqueId = Math.floor(100000 + Math.random() * 900000);
    const timestamp = Date.now();
    const randomStr = Math.random().toString(36).substring(2, 8);

    const uniqueName = `${randomTitel} #${uniqueId}-${timestamp}-${counter}-${randomStr}`;

    try {
      await fetch("https://febel.ch/ass/edit.php", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
          name: uniqueName,
          text: `Hallo vom Turbo-Bot! #${counter} – ${new Date().toLocaleString('de-CH')}`
        })
      });
      
      console.log(`Gesendet #${counter}: ${uniqueName}`);
    } catch (err) {
      console.error("Fehler:", err);
    }

    // KEINE Wartezeit mehr → maximale Geschwindigkeit
  }
}

spamFebel(); // los geht’s
