import os
import re
import csv
from collections import defaultdict

def analyze_fallbacks_from_folder(folder_path):
    fallback_counts = defaultdict(int)
    total_counts = defaultdict(int)
    
    fallback_pattern = re.compile(r"\[Fallback\]\s+(\w+)\(\):")
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") or filename.endswith(".log"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    match = fallback_pattern.search(line)
                    if match:
                        func_name = match.group(1)
                        fallback_counts[func_name] += 1
                    for function_name in ["negate_claim", "sentiment_shift", "change_to_question"]:
                        if function_name in line:
                            total_counts[function_name] += 1
    
    return fallback_counts, total_counts

def export_fallbacks_to_csv(fallback_counts, total_counts, output_path):
    with open(output_path, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Function", "Total Attempts", "Fallback Count", "Fallback Rate (%)"])
        
        functions = sorted(set(list(fallback_counts.keys()) + list(total_counts.keys())))
        for func in functions:
            total = total_counts.get(func, 0)
            fallbacks = fallback_counts.get(func, 0)
            fallback_rate = (fallbacks / total) * 100 if total > 0 else 0
            writer.writerow([func, total, fallbacks, f"{fallback_rate:.2f}%"])

log_folder_path = "logs"
output_csv_path = "fallback_summary.csv"


fallback_counts, total_counts = analyze_fallbacks_from_folder(log_folder_path)
export_fallbacks_to_csv(fallback_counts, total_counts, output_csv_path)

print(f"Relatório exportado para: {output_csv_path}")
