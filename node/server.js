import express from "express";
const app = express();
import creation from "./main.js";
app.get("/blink", creation.blink);
app.listen(5000, () => {
  console.log("App is listening on port 5000");
});
