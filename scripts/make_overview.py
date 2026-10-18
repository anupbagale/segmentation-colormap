"""Make docs/overview.png, the figure at the top of the README.

Run from the repository root:  python scripts/make_overview.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import nibabel as nib  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

root = Path(__file__).resolve().parents[1]
out = root / "docs" / "overview.png"
out.parent.mkdir(exist_ok=True)

t1 = np.asarray(nib.as_closest_canonical(nib.load(root / "data" / "T1.mgz")).dataobj)
seg = np.asarray(nib.as_closest_canonical(nib.load(root / "data" / "aseg.mgz")).dataobj).astype(int)

names, table = {}, np.zeros((256, 4))
for line in open(root / "data" / "aseg_lut.txt"):
    if line.startswith("#") or not line.strip():
        continue
    label, name, r, g, b, _ = line.split()
    names[int(label)] = name
    table[int(label)] = [int(r) / 255, int(g) / 255, int(b) / 255, 0 if label == "0" else 0.7]
colours = table[seg]

views = [("axial", 2, 50), ("coronal", 1, 43), ("sagittal", 0, 33)]
fig, ax = plt.subplots(1, 3, figsize=(15, 5.4))
shown = {}
for a, (title, axis, k) in zip(ax, views):
    a.imshow(np.take(t1, k, axis=axis).T, cmap="gray", origin="lower")
    a.imshow(np.take(colours, k, axis=axis).transpose(1, 0, 2), origin="lower")
    a.set_title(title)
    a.axis("off")
    for label in np.unique(np.take(seg, k, axis=axis)):
        if label:
            shown.setdefault(names[label].replace("Left-", "").replace("Right-", ""), table[label, :3])

fig.legend(handles=[Patch(color=c, label=n) for n, c in shown.items()],
           loc="lower center", ncol=6, frameon=False, fontsize=9)
fig.tight_layout(rect=(0, 0.14, 1, 1))
fig.savefig(out, dpi=110, bbox_inches="tight")
print("wrote", out)
