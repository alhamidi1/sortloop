# SortLoop — Material Intelligence
A working CNN-assisted recycling intake pilot. English UI, public static hosting, browser-only photo inference and locally persisted reviewed intake metadata.

## Run the system
Use Node.js 20+ and Python 3.11+. `npm ci`, then `npm run build`. Serve `dist/` with any static web server (e.g. `python -m http.server 8080 --directory dist`) and open localhost:8080. Production requires HTTPS. The 3.6 MB ONNX model and 10.7 MB WASM runtime are bundled; no inference API key is needed. First use requires downloading these assets. Browser-local data does not sync across devices.

## Reproduce training
1. Create a Python virtual environment and install `ml/requirements.txt` (CPU torch wheels can be installed from https://download.pytorch.org/whl/cpu).
2. Download https://github.com/garythung/trashnet/raw/master/data/dataset-resized.zip and unzip it.
3. Run `DATASET_DIR=/absolute/path/dataset-resized python ml/train.py` from this project. The first run downloads ImageNet MobileNetV3-Small weights.
4. The script removes SHA-256 exact duplicates, makes deterministic stratified 70/15/15 splits with seed 42, trains a frozen CNN plus a learned linear head for 80 epochs, chooses validation-loss checkpoint and evaluates once on the held-out test set.
5. Outputs are `dist/metrics.json`, `dist/model/sortloop.onnx`, `ml/model.pt`, `ml/head.pt`, `ml/splits.json`, and `ml/export-check.json`.
Training code is also available as `ml/SortLoop.ipynb`. Report charts/build use `python ml/make_report.py` (requires reportlab and matplotlib).

## Model and measured results
MobileNetV3-Small feature extractor: 927,008 frozen parameters. New 576→6 head: 3,462 trained parameters. 160×160 RGB input. 2,524 images after 3 exact duplicates removed. Train 1,766; validation 379; test 379. Selected epoch 9. Test accuracy 84.43%, macro F1 82.61%. These are random image-split TrashNet results, not site-level/field validation. Near duplicates and repeated objects may remain.

## Product scope
Upload or select a test-set sample → run real local CNN inference → review top scores → override material if needed → optionally record kilograms → explicitly confirm → save local intake → filter/page/export CSV. Public access does not mean shared records. No signup, payments, shared database, computer vision detection boxes, hazardous-material assessment or automatic recycling verdict.

## Test
`npm test` runs DOM workflow checks and real ONNX WebAssembly inference parity against Python. Browser rendering, mobile touch and full accessibility testing were not available in the build environment; DOM tests do not establish those guarantees. See VERIFICATION.md.

## Business and academic deliverables
`dist/report.pdf` maps to all five assignment sections and contains measured charts, architectural details, limitations, a business pilot plan and the full training code. No submission was made on behalf of the user. Review and adapt authorship/details to course requirements. Pricing and economics in the report are explicitly hypotheses.

## Source ownership
`src/` owns UI source; `npm run build` copies it into `dist/`. Model/evaluation/report assets remain in `dist/`. DESIGN.md and UX-CONTRACT.md document visual and behavioral contracts. OpenAI Sites deployment metadata is local and excluded from this source repository. For independent hosting, deploy the static `dist/` folder.

## Sources and attribution
- TrashNet: Gary Thung and Mindy Yang, https://github.com/garythung/trashnet (dataset, 2016). Upstream MIT license is retained as ml/DATASET-LICENSE.txt. Confirm dataset/weight rights for the intended commercial distribution before commercialization.
- Howard et al., Searching for MobileNetV3 (2019), https://arxiv.org/abs/1905.02244.
- Torchvision MobileNetV3 docs: https://docs.pytorch.org/vision/stable/models/mobilenetv3.html.
- ONNX Runtime: https://onnxruntime.ai/docs/tutorials/web/ (MIT; vendor license included).
- This project is a new implementation and does not reproduce TrashNet authors' original model or reported results.
