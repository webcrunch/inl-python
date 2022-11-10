import path from "path";
import express from "express";
import five from "johnny-five";
const board = new five.Board({ port: "COM5" });
const app = express();
app.use(express.json());
const server = (rgb) => {
  // custom color function is done
  // an check if we sent in hex parameters instead of color name
  app.get("/color/:color", async (req, res) => {
    const color = req.params.color;
    if (color.startsWith("#")) {
      if (color.length == 7) {
        rgb.color(req.params.color); //3,6,5  cyan: 00ff00,  yellow: ff0000, green: ff00ff
        res.status(200).json({ colorchanged: true });
      } else res.status(404).json({ error: "Bad color insertion." });
    } else if (!color.includes(req.params.color))
      res.status(404).json({ error: "not the right color." });
    else {
      if (color.length == 6) {
        rgb.color(`"#"${req.params.color}`); //3,6,5  cyan: 00ff00,  yellow: ff0000, green: ff00ff
        res.status(200).json({ colorchanged: true });
      } else res.status(404).json({ error: "not the right color code." });
    }
  });

  function padZero(str, len) {
    len = len || 2;
    const zeros = new Array(len).join("0");
    return (zeros + str).slice(-len);
  }

  app.get("/off", (req, res) => {
    rgb.off();
    res.status(200).json({ data: "off" });
  });

  app.get("/on", (req, res) => {
    // rgb.color(color_dict["white"]);
    rgb.on();
    res.status(200).json(true);
  });

  // app.post("/morseCode", async (req, res) => {
  //   let sentence = [];
  //   for (let i = 0; i < req.body.sequence.length; i++) {
  //     console.log(req.body.sequence[i]);
  //   }
  //   // let words = rgb.blink();
  //   res.json(true);
  // });
  // app.get("/blink/:sequence?", async (req, res) => {
  //   for (let i = req.params.sequence * 2; i >= 0; i--) {
  //     // let milisec = req.params.sequence != undefined ? req.params.sequence : 800;
  //     // let nIntervId = setInterval(() => {
  //     //   rgb.toggle();
  //     // }, 1000);
  //     // rgb.toggle();
  //     // console.log(i);
  //     // sleep(500);
  //     blink(500);
  //   }

  //   res.status(200).json({ status: true });
  // });

  const sleep = (ms) => {
    return new Promise((resolve) => setTimeout(resolve, ms));
  };

  const blink = (ms) => {
    return sleep(ms).then(rgb.toggle());
  };

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
  //const rgb = new five.Led.RGB([3, 5, 6]);
  const rgb = new five.Led.RGB({
    pins: {
      red: 3,
      green: 5,
      blue: 6,
    },
    isAnode: true,
  });

  server(rgb);
});

let __dirname = path.resolve();
let pythonPath = path.join(__dirname, "../python");
app.use(express.static(pythonPath));

app.listen(5000, () => {
  console.log("App is listening on port 5000");
});
