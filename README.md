# Knowledge Club 3D

A scroll-driven 3D version of the knowledgeclub.com homepage, built with Three.js.

- `index.html`: the source page. It loads `assets/` and `vendor/three.min.js` locally and works offline (except Google Fonts).
- `knowledgeclub-3d.html`: a single-file build that loads three.js from cdnjs and the photos from knowledgeclub.com.
- `build.py`: regenerates `knowledgeclub-3d.html` from `index.html`. Run `python3 build.py` after editing.
