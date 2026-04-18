import os

def collect_py_files(root_dir, output_txt):
    with open(output_txt, "w", encoding="utf-8") as out_file:
        for foldername, subfolders, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".py"):
                    file_path = os.path.join(foldername, filename)

                    # Avoid including the output file itself
                    if os.path.abspath(file_path) == os.path.abspath(output_txt):
                        continue

                    out_file.write(f"# FILE: {file_path}\n")
                    out_file.write("-" * 80 + "\n")

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="replace") as py_file:
                            out_file.write(py_file.read())
                    except Exception as e:
                        out_file.write(f"[Error reading file: {e}]")

                    out_file.write("\n\n")  # space between files


if __name__ == "__main__":
    directory_to_scan = "C:\\SKRepo\\OPETreeWB"
    output_file = "all_python_code.txt"

    collect_py_files(directory_to_scan, output_file)
    print("Done! Python files have been consolidated.")
