fetch("https://febel.ch/ass/edit.php", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded"
  },
  body: new URLSearchParams({
      name: "Du bisch en guete",
    text: "Hallo, dies ist der neue Inhalt!"
  })
})
  .then(r => r.text())
  .then(console.log)
  .catch(console.error);
