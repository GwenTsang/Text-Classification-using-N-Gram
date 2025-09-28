#!/usr/bin/env python3
"""
analyze_corpus.py

Reads a corpus file where each line starts with a label ('eng' or 'deu'),
a single space, then the sentence text.

Writes a CSV (header: label,sentence,th_count,ch_count) counting occurrences
of the bigrams "th" and "ch" (case-insensitive) in each sentence.

Usage:
    python3 analyze_corpus.py --input corpus.txt --output analysis.csv
"""
import csv
import argparse
import sys

def count_bigram(s: str, bigram: str) -> int:
    """Count occurrences of `bigram` in `s` using a sliding window (case-insensitive)."""
    s_lower = s.lower()
    b = bigram.lower()
    if len(b) != 2:
        raise ValueError("This function expects a 2-character bigram.")
    return sum(1 for i in range(len(s_lower) - 1) if s_lower[i:i+2] == b)

def process_file(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8", newline="") as fout:

        writer = csv.writer(fout)
        # Write header exactly as requested
        writer.writerow(["label", "sentence", "th_count", "ch_count"])

        for lineno, raw_line in enumerate(fin, start=1):
            line = raw_line.rstrip("\n")
            if not line.strip():
                # skip empty lines
                continue

            # Split into label and sentence at first space
            if " " not in line:
                # malformed line — print warning and skip
                print(f"Warning: skipping malformed line {lineno}: no space found", file=sys.stderr)
                continue

            label, sentence = line.split(" ", 1)
            label = label.strip()
            sentence = sentence.strip()

            # Optionally validate label (you can remove this check if not needed)
            if label not in ("eng", "deu"):
                print(f"Warning: line {lineno} has unexpected label '{label}' (expected 'eng' or 'deu')", file=sys.stderr)
                # proceed anyway

            th_count = count_bigram(sentence, "th")
            ch_count = count_bigram(sentence, "ch")

            writer.writerow([label, sentence, th_count, ch_count])

def main():
    parser = argparse.ArgumentParser(description="Analyze corpus for 'th' and 'ch' bigrams and produce CSV.")
    parser.add_argument("--input", "-i", default="corpus.txt", help="Input text file (default: corpus.txt)")
    parser.add_argument("--output", "-o", default="analysis.csv", help="Output CSV file (default: analysis.csv)")
    args = parser.parse_args()

    try:
        process_file(args.input, args.output)
        print(f"Wrote analysis to: {args.output}")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
