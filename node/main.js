// const { Board, Led } = require("johnny-five");
// const board = new Board({ port: "COM5" });

// // The board's pins will not be accessible until
// // the board has reported that it is ready
// board.on("ready", () => {
//   console.log("Ready!");
//   const led = new Led(11);
//   // const blue = new Led(11);
//   // const green = new Led(10);
//   // const red = new Led(9);
//   // red.fadeOut(2000);
//   led.fade(10);
//   // green.blink(500);
//   // blue.blink(500);
//   //led.pulse();
//   board.wait(6000, () => {
//     // stop() terminates the interval
//     // off() shuts the led off
//     led.stop().off();
//   });
// });

// const temporal = require("temporal");
import five from "johnny-five";
// const { Board, Led } = require("johnny-five");
// const board = new five.Board({ port: "COM5" });
// const board = new five.Board();
// board.on("ready", () => {
//
//   let index = 0;
//   const rainbow = [
//     "FF0000",
//     "FF7F00",
//     "FFFF00",
//     "00FF00",
//     "0000FF",
//     "4B0082",
//     "8F00FF",
//   ];

//   board.loop(1000, () => {
//     rgb.color(rainbow[index++]);
//     if (index === rainbow.length) {
//       index = 0;
//     }
//   });
// });

const blink = () => {
  //   board.on("ready", () => {
  //     const rgb = new five.Led.RGB([6, 5, 3]);
  //     rgb.blink;
  //   });
};

export default {
  blink,
};
