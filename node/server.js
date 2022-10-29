import express from "express";
import five from "johnny-five";
const board = new five.Board({ port: "COM5" });
const app = express();
app.use(express.json());
const server = (rgb) => {
  // custom color function is done
  app.post("/color", async (req, res) => {
    if (req.body.color.length < 7)
      res.status(404).json({ error: "Bad color insertion" });
    else {
      rgb.color(req.body.color);
      res.status(200).json({ colorchanged: true });
    }
  });

  app.get("/off", (req, res) => {
    rgb.color("#FFFFFF");
    res.status(200).json(true);
  });

  app.get("/on", (req, res) => {
    rgb.color("#000000");
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

  app.get("/blink/:sequence?", async (req, res) => {
    rgb.blink(req.params.sequence);
    res.json(true);
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
      red: 6,
      green: 5,
      blue: 3,
    },
  });

  server(rgb);
});

app.listen(5000, () => {
  console.log("App is listening on port 5000");
});
