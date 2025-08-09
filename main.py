import os
import csv

def load_careers(file_path):
    careers = []
    print(f"Loading careers from: {file_path}")
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                skills = [skill.strip().lower() for skill in row['skills'].split(';')]
                careers.append({
                    'career': row['career'],
                    'skills': skills
                })
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []
    except PermissionError:
        print(f"Error: Permission denied when accessing {file_path}")
        return []
    except Exception as e:
        print(f"Error loading careers file: {e}")
        return []
    return careers

def read_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            print(f"Unsupported file format: {ext}. Currently only .txt is supported.")
    except FileNotFoundError:
        print(f"Error: Resume file not found - {file_path}")
    except PermissionError:
        print(f"Error: Permission denied when accessing resume file {file_path}")
    except Exception as e:
        print(f"Error reading resume file: {e}")
    return text.lower()

def match_career(resume_text, careers):
    best_match = None
    best_score = 0
    missing_skills = []

    for career in careers:
        matched = [skill for skill in career['skills'] if skill in resume_text]
        if len(career['skills']) == 0:
            continue
        score = len(matched) / len(career['skills'])
        if score > best_score:
            best_score = score
            best_match = career['career']
            missing_skills = [skill for skill in career['skills'] if skill not in matched]

    return best_match, best_score, missing_skills

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())

    careers_file = os.path.join("data", "careers.csv")
    careers = load_careers(careers_file)
    if not careers:
        print("No careers loaded. Please check the careers file path and ensure it exists.")
        exit(1)

    resume_path = input("Enter resume file path (only .txt supported currently): ").strip()
    resume_text = read_resume(resume_path)

    if resume_text:
        career, score, missing = match_career(resume_text, careers)
        if career:
            print(f"\n=== Career Recommendation ===")
            print(f"Best Match: {career} — {score * 100:.1f}% match")
            if missing:
                print("Missing skills to acquire:", ", ".join(missing))
            else:
                print("You have all the required skills!")
        else:
            print("No suitable career match found.")
    else:
        print("Could not read resume text. Please check your file and try again.")
