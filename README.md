# 🌱 AgriScan.ai

**Scan Leaves. Detect Diseases. Protect Crops.**
*Smart Agriculture • Artificial Intelligence • Deep Learning*

AgriScan.ai – An intelligent AI-powered platform that detects crop diseases from leaf images and provides useful agricultural guidance to help farmers protect their crops.

Farmers upload or capture a photo of a leaf. A **YOLO26n-cls** model fine-tuned on the **PlantVillage** dataset (38 classes: 14 crops, healthy and diseased) predicts the condition. The app then shows the disease name, confidence score, symptoms, treatment and prevention guidance. An **n8n** workflow ties the upload, model call and response together.

The full problem statement is in [`docs/problem_statement.md`](docs/problem_statement.md).

## How it works

```
Browser (upload / camera)
        │  POST /api/analyze
        ▼
   Flask app ───────────► n8n webhook ──► Flask /api/predict (YOLO26n-cls)
        ▲                      │                    │
        │                      └── confidence check ◄┘
        └──────────── JSON: disease, confidence, symptoms, treatment ◄──
```

If `N8N_WEBHOOK_URL` is not set (or n8n is down) the app runs the model directly, so it always works.

## Project layout

```
agriscan-ai/
├── agriscan/             web app package
│   ├── predictor.py      loads YOLO26n-cls, returns top-3 predictions
│   ├── advice.py         maps a class to symptoms / treatment text
│   ├── webapp.py         Flask routes
│   ├── data/disease_info.json   curated guidance for 26 diseases
│   ├── templates/ static/       the web page
├── scripts/
│   ├── prepare_dataset.py   PlantVillage -> train/val/test
│   ├── train.py             fine-tune YOLO26n-cls
│   ├── evaluate.py          test accuracy + per-class report
│   └── predict_cli.py       one-off prediction from terminal
├── n8n/agriscan_workflow.json   import this into n8n
├── tests/                pytest tests (no model needed)
├── config.py             paths and settings
├── run.py                start the web server
├── Dockerfile, docker-compose.yml
└── docs/
```

## Quick start

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get and prepare PlantVillage

Either download it yourself from Kaggle ("PlantVillage Dataset", by abdallahalidev), unzip it, then:

```bash
python scripts/prepare_dataset.py --source path/to/unzipped/folder
```

or let the script fetch it (needs a Kaggle API token set up):

```bash
python scripts/prepare_dataset.py --download
```

This makes an 80/10/10 train/val/test split in `data/plantvillage/`.

### 3. Train

```bash
python scripts/train.py --epochs 25 --batch 64
```

A GPU is strongly recommended (a free Colab or Kaggle T4 takes roughly 20-40 minutes). On CPU, add `--device cpu` and expect it to be much slower; lower `--epochs` if you are in a hurry.
The best weights are copied to `models/agriscan_yolo26n_cls.pt` automatically.

### 4. Evaluate

```bash
python scripts/evaluate.py
```

Fill in your own numbers in the table below after training.

| Metric | Value |
| --- | --- |
| Top-1 accuracy (test) | _your result_ |
| Top-5 accuracy (test) | _your result_ |

### 5. Run the app

```bash
python run.py
```

Open http://localhost:5000, upload a leaf photo and press **Scan leaf**.

Check a single image from the terminal:

```bash
python scripts/predict_cli.py sample_leaf.jpg
```

## n8n workflow

1. Start everything: `docker compose up --build` (n8n is at http://localhost:5678).
2. In n8n choose **Import from file** and pick `n8n/agriscan_workflow.json`.
3. **Activate** the workflow (toggle at top right). The production webhook is `http://n8n:5678/webhook/agriscan`, which is already set in `docker-compose.yml`.

If you run n8n outside Docker, change the URL in the *Run YOLO26n Model* node to wherever the Flask app is (for example `http://localhost:5000/api/predict`) and export `N8N_WEBHOOK_URL=http://localhost:5678/webhook/agriscan` before `python run.py`.

Workflow steps: **Receive Leaf Image → Run YOLO26n Model → Confident Enough? → Send Diagnosis / Send With Low-Confidence Warning**.

## Settings

| Variable | Default | Meaning |
| --- | --- | --- |
| `AGRISCAN_MODEL` | `models/agriscan_yolo26n_cls.pt` | path to trained weights |
| `AGRISCAN_CONFIDENCE` | `0.60` | below this the result is flagged unreliable |
| `N8N_WEBHOOK_URL` | empty | send images through n8n when set |
| `PORT` | `5000` | web server port |

## Tests

```bash
pytest
```

The tests use a stand-in model, so they run without any weights or dataset.

## Known limits (be honest about these in your report)

- PlantVillage photos are taken on plain backgrounds in a lab. Accuracy on messy real-field photos is noticeably lower than the test-split accuracy, so keep the confidence warning and encourage close-up single-leaf photos.
- Only the 14 crops / 38 classes in PlantVillage are supported. Indian staples like rice and wheat would need extra data.
- Treatment text in `disease_info.json` is general guidance compiled from standard agricultural extension material. Doses and approved chemicals vary by region, so users are told to follow product labels and consult local experts (KVK / agriculture officer). Have a domain expert review it before real-world use.

## Tech stack

Python · Ultralytics YOLO26n-cls · PlantVillage · Flask · n8n · Docker · HTML/CSS/JS

## License

For academic / educational use. PlantVillage is released under its own terms, check the dataset page before commercial use.
