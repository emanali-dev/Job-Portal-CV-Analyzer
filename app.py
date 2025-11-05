import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from utils.analyzer import analyze_text
from utils.batch_runner import run_batch
from utils.file_reader import read_pdf, read_docx

app = Flask(__name__)

# ------------------- PATHS -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATASET_FOLDER = os.path.join(BASE_DIR, "DataSet")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
JOB_DESC_FOLDER = os.path.join(BASE_DIR, "job_descriptions")

# ensure folders exist
for folder in [UPLOAD_FOLDER, DATASET_FOLDER, RESULTS_FOLDER, JOB_DESC_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ------------------- HELPERS -------------------
def load_keywords_for_role(role):
    path = os.path.join(JOB_DESC_FOLDER, f"{role}.txt")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read().strip()
    if "," in txt:
        kws = [k.strip() for k in txt.split(",") if k.strip()]
    else:
        kws = [line.strip() for line in txt.splitlines() if line.strip()]
    return kws

# ------------------- PAGE ROUTES -------------------
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/single')
def single_page():
    return render_template('single.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/batch')
def batch_page():
    return render_template('index.html')  

# ------------------- KEYWORDS -------------------
@app.route('/keywords', methods=['GET'])
def keywords():
    role = request.args.get('role', '')
    if not role:
        return jsonify({"keywords": []})
    return jsonify({"keywords": load_keywords_for_role(role)})

# ------------------- SINGLE CV ANALYSIS -------------------
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'cv' not in request.files:
        return jsonify({"error": "No file uploaded under key 'cv'"}), 400

    file = request.files['cv']
    filename = file.filename
    if not filename:
        return jsonify({"error": "Uploaded file has no filename"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    form_keywords = request.form.get('keywords', '').strip()
    role = request.form.get('role', '').strip()

    if form_keywords:
        job_keywords = [k.strip() for k in form_keywords.split(',') if k.strip()]
    elif role:
        job_keywords = load_keywords_for_role(role)
    else:
        return jsonify({"error": "No keywords or role provided"}), 400

    if not job_keywords:
        return jsonify({"error": "No keywords resolved for analysis"}), 400

    try:
        text = read_pdf(save_path) if filename.lower().endswith('.pdf') else read_docx(save_path)
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {e}"}), 500

    if not text.strip():
        return jsonify({"error": "Uploaded file contains no readable text"}), 400

    try:
        results = analyze_text(text, job_keywords)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {e}"}), 500

    return jsonify(results)

# ------------------- BATCH ANALYSIS -------------------
@app.route('/batch_runner', methods=['POST'])
def batch_runner_route():
    payload = request.get_json() or {}
    role = (payload.get('role') or '').strip()
    raw_keywords = (payload.get('keywords') or '').strip()

    if raw_keywords:
        job_keywords = [k.strip() for k in raw_keywords.split(',') if k.strip()]
    elif role:
        job_keywords = load_keywords_for_role(role)
    else:
        return jsonify({"error": "No role or keywords provided."}), 400

    if not job_keywords:
        return jsonify({"error": f"No keywords found for role '{role}'"}), 400

    try:
        summary = run_batch(DATASET_FOLDER, job_keywords)
    except Exception as e:
        return jsonify({"error": f"Batch failed: {e}"}), 500

    if isinstance(summary, dict):
        summary.setdefault("num_files", len(summary.get("results", [])))
        summary.setdefault("num_successful", len(summary.get("results", [])))
    else:
        summary = {
            "num_files": len(summary),
            "num_successful": len(summary),
            "results": summary
        }

    return jsonify(summary), 200

# ------------------- PERFORMANCE ANALYSIS -------------------
@app.route('/performance/<path:filename>')
def performance_page(filename):
    keywords = request.args.get('keywords', '')
    job_keywords = [k.strip() for k in keywords.split(',') if k.strip()]

    file_path = os.path.join(DATASET_FOLDER, filename)
    if not os.path.exists(file_path):
        return f"File not found: {filename}", 404

    try:
        text = read_pdf(file_path) if filename.lower().endswith('.pdf') else read_docx(file_path)
        results = analyze_text(text, job_keywords)
    except Exception as e:
        return f"Analysis failed: {e}", 500

    return render_template(
        'performance.html',
        candidate=os.path.splitext(filename)[0],
        filename=filename,
        keywords=job_keywords,
        results=results
    )

# ------------------- FILE SERVING -------------------
@app.route('/uploads/<path:filename>')
def serve_uploaded(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/dataset/<path:filename>')
def serve_dataset(filename):
    return send_from_directory(DATASET_FOLDER, filename)

# ------------------- RUN -------------------
if __name__ == '__main__':
    app.run(debug=True)
