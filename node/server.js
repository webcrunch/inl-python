import path from "path";
import express from "express";
import five from "johnny-five";
const board = new five.Board({ port: "COM5" });
const color_dict = {
  black: "#ffffff",
  white: "#000000",
  green: "#ff00ff",
  red: "#ffff00",
  blue: "#00ffff",
  purple: { R: 0, G: 1, B: 0 },
  yellow: "#ff0000",
  cyan: { R: 0, G: 0, B: 1 },
};
const colors = [
  "red",
  "green",
  "blue",
  "purple",
  "yellow",
  "cyan",
  "white",
  "black",
];
const app = express();
app.use(express.json());
const server = (rgb) => {
  // custom color function is done
  // an check if we sent in hex parameters instead of color name
  app.get("/color/:color", async (req, res) => {
    if (req.params.color.startsWith("#")) {
      if (req.params.color.length == 7) {
        rgb.color(req.params.color); //3,6,5  cyan: 00ff00,  yellow: ff0000, green: ff00ff
        res.status(200).json({ colorchanged: true });
      } else res.status(404).json({ error: "Bad color insertion." });
    } else if (!colors.includes(req.params.color))
      res.status(404).json({ error: "not the right color." });
    else {
      rgb.color(color_dict[req.params.color]); //3,6,5  cyan: 00ff00,  yellow: ff0000, green: ff00ff
      res.status(200).json({ colorchanged: true });
    }

    //     # 6,5 RED
    // # 3,6 GREEN
    // # 3,5 BLUE
    // # 5 PURPLE
    // # 6 YELLOW
    // # 3 CYAN
    // # 0,0,0 WHITE
    // # 1,1,1 BLACK
  });

  app.get("/off", (req, res) => {
    rgb.color(color_dict["black"]);
    res.status(200).json(true);
  });

  app.get("/on", (req, res) => {
    rgb.color(color_dict["white"]);
    res.status(200).json(true);
  });

  app.post("/morseCode", async (req, res) => {
    let sentence = [];
    for (let i = 0; i < req.body.sequence.length; i++) {
      console.log(req.body.sequence[i]);
    }
    // let words = rgb.blink();
    res.json(true);
  });

  app.get("/rainbow", (req, res) => {
    let rainbow;
    let lastColor = "ff0000";
    let red = 255,
      green = 0,
      blue = 0,
      s = 0;
    clearInterval(rainbow);
    rainbow = setInterval(function () {
      switch (s) {
        case 0:
          red -= 1;
          green += 1;
          if (red == 0) {
            s = 1;
          }
          break;
        case 1:
          green -= 1;
          blue += 1;
          if (green == 0) {
            s = 2;
          }
          break;
        case 2:
          blue -= 1;
          red += 1;
          if (blue == 0) {
            s = 0;
          }
          break;
      }
      let a = red + "," + green + "," + blue;
      a = a.split(",");
      let b = a.map(function (x) {
        x = parseInt(x).toString(16);
        return x.length == 1 ? "0" + x : x;
      });

      b = "" + b.join("");

      rgb.color(b);
      lastColor = b;
    }, 10);

    res.json({ status: true });
  });

  app.get("/blink/:sequence?/", async (req, res) => {
    rgb.blink(req.params.sequence != undefined ? req.params.sequence : 1000);
    res.status(200).json({ status: true });
  });

  //   app.get("/power/:status", async (req, res) => {
  //     console.log(req.params.status);
  // );
  //     // req.params.status === "on" ? rgb.on() : rgb.off();
  //     res.json(true);
  //   });
};

// import { color } from "./main.js";
// app.get("/blink", creation.blink);

// });

board.on("ready", () => {
  console.log("board ready ");
  //   const rgb = new five.Led.RGB([6, 5, 3]);
  const rgb = new five.Led.RGB({
    pins: {
      red: 3,
      green: 5,
      blue: 6,
    },
  });

  server(rgb);
});

let __dirname = path.resolve();
let pythonPath = path.join(__dirname, "../python");
app.use(express.static(pythonPath));

app.listen(5000, () => {
  console.log("App is listening on port 5000");
});
