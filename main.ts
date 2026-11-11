// Cutest Cat v2 entry (Node 22, standard library only): the cat in
// entry.png was drawn with code (draw.py, PIL: a ginger kitten with huge
// glossy eyes, a tongue blep, a daisy crown, hugging a smiling blue
// plush fish, toe-bean paws), and this program copies it to
// /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
// and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
