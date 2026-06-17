/* =============================================================
   MODULE 2 — Image Captioning (simulated BLIP / BLIP-2 / LLaVA)
   -------------------------------------------------------------
   Turns the Computer-Vision detection into a natural-language
   caption describing the scene, e.g.
   "Lionel Messi celebrates after scoring during Argentina's victory."
   ============================================================= */

const Captioning = {
  caption(img, det) {
    switch (img.type) {
      case "match": {
        const scene = det.celebration
          ? `players of ${det.team} celebrate a goal`
          : `${img.home} and ${img.away} battle for the ball`;
        const crowd = det.crowd ? " in front of a packed crowd" : "";
        return capitalize(`${scene}${crowd} during the World Cup clash between ${img.home} and ${img.away}.`);
      }
      case "team":
        return `The ${img.team} national team lines up for the team photo before kick-off.`;
      case "player": {
        const p = img.player;
        return `${p.name} of ${p.team} poses in the national jersey, ready for the World Cup.`;
      }
      case "stadium":
        return `A wide view of ${img.stadium.name} in ${img.stadium.city}, one of the FIFA World Cup 2026 host venues.`;
      case "fan":
        return `Passionate ${img.team} fans wave flags and celebrate in the stands.`;
      default:
        return "A scene from the FIFA World Cup 2026.";
    }
  }
};

function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
