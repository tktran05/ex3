/* =============================================================
   MODULE 1 — Computer Vision (simulated YOLO / Detectron2 style)
   -------------------------------------------------------------
   In a production build this layer would run YOLOv8 / Grounding DINO
   / Florence-2 on real FIFA images. Here we deterministically
   "detect" objects from the image's metadata so the rest of the
   pipeline receives the exact JSON contract from the spec:

     { "players": 14, "ball": true, "celebration": true, "team": "Argentina" }
   ============================================================= */

const Vision = {
  /* Detect objects for a given image descriptor.
     `img` carries a `type` and contextual teams/player so the mock
     detector can produce plausible, type-appropriate output.        */
  analyze(img) {
    const t = img.type;
    let out = {
      players: 0,
      ball: false,
      crowd: false,
      celebration: false,
      jerseyColors: [],
      team: img.team || null,
      objects: []
    };

    if (t === "match") {
      out.players = randInt(8, 16);
      out.ball = true;
      out.crowd = true;
      out.celebration = Math.random() > 0.4;
      out.jerseyColors = [teamColor(img.home, 0), teamColor(img.away, 0)];
      out.team = out.celebration ? (img.winner || img.home) : img.home;
      out.objects = ["players", "ball", "goalpost", "referee", "crowd"];
    } else if (t === "team") {
      out.players = 11;
      out.crowd = false;
      out.jerseyColors = [teamColor(img.team, 0)];
      out.objects = ["players", "team-line-up", "flag"];
    } else if (t === "player") {
      out.players = 1;
      out.jerseyColors = [teamColor(img.team, 0)];
      out.objects = ["player", "jersey", "boots"];
    } else if (t === "stadium") {
      out.players = 0;
      out.crowd = true;
      out.objects = ["stadium", "pitch", "stands", "floodlights", "roof"];
    } else if (t === "fan") {
      out.players = 0;
      out.crowd = true;
      out.celebration = true;
      out.jerseyColors = [teamColor(img.team, 0)];
      out.objects = ["fans", "flags", "banners", "face-paint"];
    }

    out.confidence = +(0.82 + Math.random() * 0.15).toFixed(2);
    return out;
  },

  /* Spec-shaped compact JSON (the exact contract in the brief) */
  toSpecJSON(detection) {
    return {
      players: detection.players,
      ball: detection.ball,
      celebration: detection.celebration,
      team: detection.team
    };
  }
};
