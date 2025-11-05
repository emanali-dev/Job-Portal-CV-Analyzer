import os
import time
from utils.file_reader import read_pdf, read_docx
from utils.analyzer import analyze_text

def run_batch(folder_path, job_keywords):
    start = time.time()
    results = []
    errors = []
    supported_exts = ('.pdf', '.docx')

    if not os.path.exists(folder_path):
        return {"error": f"Dataset folder not found: {folder_path}"}

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]
    if not files:
        return {"error": "No CV files found in dataset folder."}

    print(f"📂 Found {len(files)} CVs in {folder_path}")

    for fname in files:
        fpath = os.path.join(folder_path, fname)
        try:
            text = read_pdf(fpath) if fname.lower().endswith('.pdf') else read_docx(fpath)
            if not text or not text.strip():
                errors.append(f"Skipped {fname}: empty text")
                continue

            analysis = analyze_text(text, job_keywords)
            avg = sum([analysis[a]["Relevance (%)"] for a in analysis]) / len(analysis)
            
            # Build record including URL for front-end
            rec = {
                "filename": fname,
                "candidate": os.path.splitext(fname)[0],
                "Average Relevance": round(avg,2),
                "url": f"/dataset/{fname}"  # this URL can be used by the front-end to open the CV
            }
            
            for a in analysis:
                rec[f"{a} - Time(s)"] = analysis[a]["Execution Time (s)"]
            
            results.append(rec)
            print(f"✅ {fname}")
        except Exception as e:
            err = f"{fname}: {e}"
            print("❌", err)
            errors.append(err)

    elapsed = round(time.time() - start, 2)
    return {
        "num_files": len(files),
        "num_successful": len(results),
        "num_failed": len(errors),
        "elapsed_time": elapsed,
        "errors": errors,
        "results": results
    }
