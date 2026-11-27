// THE WORLD TODAY — news-image-20261127 entrypoint (Node 22, stdlib only).
// The front page is pre-drawn at build time by draw.py (Pillow) into the
// entry.png beside this file. This program only copies it into the output
// directory the grader reads: $MAKEFUN_OUTPUT_DIR, or /output by default.
// It never deletes anything: it only creates the directory if missing.
// The copy is byte-for-byte, so running it twice gives identical output.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL("./entry.png", import.meta.url),
  join(outDir, "entry.png"),
);
