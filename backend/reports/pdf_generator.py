import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_analytics_report(csv_path: str, output_pdf_path: str):
    df = pd.read_csv(csv_path)
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    # Render response time graph
    plt.figure(figsize=(9, 4))
    plt.plot(df["sequence"], df["request_time_ms"], color='#0d6efd', linewidth=1.5)
    plt.title("Latency Trend Across Requests")
    plt.xlabel("Request Sequence")
    plt.ylabel("Response Time (ms)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    graph_path = output_pdf_path.replace(".pdf", "_chart.png")
    plt.savefig(graph_path, dpi=150)
    plt.close()
    
    # Build PDF
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Performance Test Analytics Report")
    c.line(50, height - 60, width - 50, height - 60)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 90, "Summary Statistics")
    
    c.setFont("Helvetica", 10)
    total_reqs = len(df)
    successes = df['success'].sum() if 'success' in df else 0
    success_rate = (successes / total_reqs * 100) if total_reqs > 0 else 0
    avg_latency = df['request_time_ms'].mean() if total_reqs > 0 else 0
    p95_latency = df['request_time_ms'].quantile(0.95) if total_reqs > 0 else 0
    
    c.drawString(50, height - 110, f"Total Requests Sent: {total_reqs}")
    c.drawString(50, height - 125, f"Successful Requests: {successes} ({success_rate:.1f}%)")
    c.drawString(50, height - 140, f"Average Response Time: {avg_latency:.2f} ms")
    c.drawString(50, height - 155, f"95th Percentile Latency: {p95_latency:.2f} ms")
    
    # Embed Graph
    if os.path.exists(graph_path):
        c.drawImage(graph_path, 50, height - 480, width=500, height=280)
        os.remove(graph_path)
        
    c.save()
    return output_pdf_path