const puppeteer = require("puppeteer");
const fs = require("fs"); 

const getMoves = async () => {
  // Startar puppeteer
  const browser = await puppeteer.launch({
    defaultViewport: null,
  });

  // öppnar en ny sida
  const page = await browser.newPage();

  // Går till sidan jag ska skrapa och väntar tills allt är laddat
  await page.goto("https://ultimateframedata.com/yoshi", {
    waitUntil: "domcontentloaded",
  });

  // Samlar all data
  let moves = await page.evaluate(() => {
    let list = [];
    //sorterar bort alla saker som inte är moves, då endast olika moves och throws har startuplag/classen startup
    let moveContainers = Array.from(
      document.querySelectorAll(".movecontainer")
    ).filter(
      (item) => item.children[2] && item.children[2].className === "startup"
    );

    //loopar igenom alla moves och skapar ett object med all information jag vill ha för varje move genom att kolla på klasser och ta bort alla tomrum (\n,\t) genom funktionen trim
    for (const move of moveContainers) {
      let name = move.querySelector(".movename").innerHTML.trim();
      let startup = move.querySelector(".startup").innerHTML.trim();
      let totalFrames = move.querySelector(".totalframes").innerHTML.trim();
      let dmg = move.querySelector(".basedamage").innerHTML.trim();
      
    //   Då throwsen saknar endlag taggen så raisas errors om vi kollar efter den taggen så vi catchar errorna och ger dem ett odefinerat värde om de inte finns vilket vi kan använda för att sortera bort dem senare
      let endLag = undefined;
      try {
        endLag = move.querySelector(".endlag").innerHTML.trim();
      } catch {}

      list.push({
        Name: name,
        Startup: startup,
        TotalFrames: totalFrames,
        EndLag: endLag,
        Damage: dmg,
      });
    }

    return list;
  });
// sorterarbort alla moves klassade som throws då jag inte vill ha kvar dem och gör arrayen så den inte har några tomma platser
  let oversize = 0;
  for (let i = 0; i < moves.length; i++) {
    if ("EndLag" in moves[i]) {
    } else {
      delete moves[i];
      oversize++;
    }
  }
  moves.length -= oversize;



// gör om mitt data till jsonformat
  const jsonData = JSON.stringify(moves);
//skriver ut datat i en jsonfil och skriver eventuellt ut i konsolen om det misslyckas
  fs.writeFile("data.json", jsonData, "utf8", (err) => {
    if (err) {
      console.error("An error ocurred while writíng to the file:", err);
      return;
    }
    console.log("Data has been written");
  });

  // stänger browsern
  await browser.close();
};

// startar skrapningen
getMoves();
