# word_frequency.py
# Analyses .txt files in a folder and reports the most frequent words
# Usage: python word_frequency.py

import os
import string
from collections import Counter

# ── Common words to ignore (called "stop words") ──
STOP_WORDS = {
    "the", "a", "an", "and", "is", "in", "it", "of", "to", "that",
    "was", "for", "on", "are", "with", "as", "at", "be", "by", "from",
    "or", "but", "not", "this", "have", "had", "they", "you", "we",
    "he", "she", "his", "her", "its", "my", "your", "our", "their",
    "been", "has", "will", "would", "could", "should", "do", "did",
    "so", "if", "up", "out", "about", "into", "than", "then", "when",
    "there", "what", "which", "who", "i", "me", "him", "us", "them",
    "all", "more", "no", "can", "one", "just", "also", "very", "some"
}


def ask_for_folder():
    """Ask the user for a folder path and check it exists."""
    folder_path = input("Enter the folder path containing your .txt files:\n> ").strip()

    # Handle common shortcuts
    if folder_path == ".":
        folder_path = os.getcwd()

    if not os.path.exists(folder_path):
        print(f"\n❌ Folder not found: {folder_path}")
        print("Please check the path and try again.")
        return None

    return folder_path


def read_txt_files(folder_path):
    """Find and read all .txt files in the folder."""
    txt_files = []

    for file in os.listdir(folder_path):
        if file.endswith(".txt") and file != "word_report.txt":
            full_path = os.path.join(folder_path, file)
            txt_files.append(full_path)

    if not txt_files:
        print("\n❌ No .txt files found in that folder.")
        return None

    print(f"\n✓ Found {len(txt_files)} file(s):")
    for f in txt_files:
        print(f"  - {os.path.basename(f)}")

    return txt_files


def combine_text(txt_files):
    """Read and combine all file contents into one string."""
    combined = ""

    for file_path in txt_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                combined += f.read() + " "
        except Exception as e:
            print(f"  ⚠ Could not read {os.path.basename(file_path)}: {e}")

    return combined


def process_text(text):
    """Clean text — remove punctuation, lowercase, split into words."""
    # Replace punctuation with spaces (not nothing — avoids words joining)
    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    cleaned = text.translate(translator).lower()

    # Split into individual words
    words = cleaned.split()

    # Remove stop words and very short words (1-2 characters)
    filtered = [w for w in words if w not in STOP_WORDS and len(w) > 2]

    return filtered


def get_top_words(words, top_n=20):
    """Count word frequencies and return the top N."""
    counter = Counter(words)
    return counter.most_common(top_n)


def display_results(top_words, total_words):
    """Print a formatted results table to the terminal."""
    print(f"\n{'─' * 40}")
    print(f"  TOP {len(top_words)} WORDS")
    print(f"  Total words analysed: {total_words:,}")
    print(f"{'─' * 40}")
    print(f"  {'RANK':<6} {'WORD':<20} {'COUNT':<8} BAR")
    print(f"{'─' * 40}")

    max_count = top_words[0][1] if top_words else 1

    for rank, (word, count) in enumerate(top_words, 1):
        # Visual bar scaled to max word
        bar_length = int((count / max_count) * 20)
        bar = "█" * bar_length
        print(f"  {rank:<6} {word:<20} {count:<8} {bar}")

    print(f"{'─' * 40}")


def save_report(top_words, total_words, folder_path, source_files):
    """Save a formatted report to word_report.txt in the same folder."""
    report_path = os.path.join(folder_path, "word_report.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("WORD FREQUENCY REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Files analysed: {len(source_files)}\n")
        for sf in source_files:
            f.write(f"  - {os.path.basename(sf)}\n")
        f.write(f"Total words: {total_words:,}\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"{'RANK':<6} {'WORD':<20} {'COUNT'}\n")
        f.write("-" * 36 + "\n")

        for rank, (word, count) in enumerate(top_words, 1):
            f.write(f"{rank:<6} {word:<20} {count}\n")

    print(f"\n✓ Report saved to: {report_path}")


# ── Main program ──
if __name__ == "__main__":
    print("\n╔══════════════════════════════════╗")
    print("║   WordFrequency Analyser v1.0    ║")
    print("╚══════════════════════════════════╝")
    print("Analyse your writing patterns.\n")

    # Step 1: Get folder
    folder = ask_for_folder()
    if not folder:
        exit()

    # Step 2: Find files
    files = read_txt_files(folder)
    if not files:
        exit()

    # Step 3: Read and combine text
    print("\n⟳ Reading files...")
    raw_text = combine_text(files)

    # Step 4: Process text
    print("⟳ Processing text...")
    words = process_text(raw_text)

    if not words:
        print("❌ No words found after processing.")
        exit()

    # Step 5: Get top words
    top_20 = get_top_words(words, top_n=20)

    # Step 6: Display results
    display_results(top_20, len(words))

    # Step 7: Save report
    save_report(top_20, len(words), folder, files)

    print("\n✓ Done! Happy writing. 🚀\n")
