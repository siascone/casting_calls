import subprocess
import os
from flask import Flask, render_template, Response, send_file

app = Flask(__name__)

# Ensure the file path is consistent
OUTPUT_FILE = "./output_files/job_descriptions.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream-scraper')
def stream_scraper():
    def generate():
        # -u is vital for real-time printing
        # We use stdbuf (on Linux/Mac) or unbuffered Python to ensure no delay
        process = subprocess.Popen(
            ["python", "-u", "scrape_performer_job_descriptions.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        yield "data: [SYSTEM]: Scraper Engine Started...\n\n"

        for line in iter(process.stdout.readline, ""):
            clean_line = line.strip()
            if clean_line:
                # Format required by EventSource
                yield f"data: {clean_line}\n\n"
        
        process.stdout.close()
        process.wait()
        
        yield "data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/get-file')
def get_file():
    if os.path.exists(OUTPUT_FILE):
        return send_file(OUTPUT_FILE, as_attachment=True)
    return "File not found. Please run the scraper first.", 404

if __name__ == '__main__':
    # Threaded=True allows the stream to run without blocking the whole server
    app.run(debug=True, port=5000, threaded=True)

# import subprocess
# import os
# from flask import Flask, render_template, Response, send_file

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/stream-scraper')
# def stream_scraper():
#     def generate():
#         # Run the script and capture STDOUT
#         process = subprocess.Popen(
#             ["python", "-u", "scrape_performer_job_descriptions.py"], # -u forces unbuffered output
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#             text=True
#         )

#         for line in iter(process.stdout.readline, ""):
#             # SSE format requires "data: " prefix and double newlines
#             yield f"{line}\n"
        
#         yield "[DONE]\n\n"

#     return Response(generate(), mimetype='text/event-stream')


# @app.route('/get-file')
# def get_file():
#     file_path = "./output_files/detailed_jobs.json"
#     if os.path.exists(file_path):
#         return send_file(file_path, as_attachment=True)
#     return "File not found", 404

# if __name__ == '__main__':
#     app.run(debug=True)