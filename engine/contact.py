# fogli di controllo: 4 fotogrammi per scena, 4 scene per foglio
import sys, os
sys.argv = [sys.argv[0], "x"] + sys.argv[1:]
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from PIL import Image
fr = (0.12, 0.38, 0.64, 0.9)
idx = [int(x) for x in sys.argv[2:]] or list(range(R.N))
tw, th = (480, 270) if R.W > R.H else (216, 384)
for b in range(0, len(idx), 4):
    sheet = Image.new("RGB", (tw * 4, th * 4))
    for r, i in enumerate(idx[b:b + 4]):
        sc, total = R.scene(i)
        for c, f in enumerate(fr):
            sheet.paste(R.frame(i, sc, int(total * f), total).resize((tw, th)), (c * tw, r * th))
    sheet.save(f"prev/c{b // 4:02d}.jpg", quality=72)
print("ok")
