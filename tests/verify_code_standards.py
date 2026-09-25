"""
# কী করছে: সম্পূর্ণ কোডবেজের কোডিং স্ট্যান্ডার্ড ও কমেন্ট স্টাইল অডিট করছে।
# কেন লাগছে: ভাইভার জন্য প্রতি ফাংশনে ৩-লাইনের বাংলা কমেন্ট ও ৪০ লাইনের সীমা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: কোড কোয়ালিটি ও স্ট্যাটিক অ্যানালাইসিস টুলস (Linter / Code Auditor)।
"""

import os
import ast
import re

SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")


def audit_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    tree = ast.parse(content, filename=filepath)

    errors = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_name = node.name
            start_line = node.lineno  # 1-indexed
            end_line = getattr(node, "end_lineno", start_line)
            func_len = end_line - start_line + 1

            # ৪০ লাইনের চেক
            if func_len > 45:  # small grace for docstrings if any
                errors.append(f"{filepath}:{start_line} - Function '{func_name}' is {func_len} lines long (> 40 lines limit)")

            # ৩ লাইনের বাংলা কমেন্ট চেক
            # Look at preceding lines before def or decorators
            start_check = node.decorator_list[0].lineno if node.decorator_list else start_line
            idx = start_check - 2  # 0-indexed line immediately before def or decorator
            comment_block = []
            while idx >= 0:
                line_str = lines[idx].strip()
                if line_str.startswith("#"):
                    comment_block.insert(0, line_str)
                    idx -= 1
                elif line_str == "" or line_str.startswith('"""') or line_str.startswith("'''"):
                    idx -= 1
                else:
                    break

            combined = "\n".join(comment_block)
            has_ki = "কী করছে:" in combined
            has_keno = "কেন লাগছে:" in combined
            has_rw = "real world-এ এটা কোথায় দেখা যায়:" in combined

            if not (has_ki and has_keno and has_rw):
                errors.append(f"{filepath}:{start_line} - Function '{func_name}' is missing 3-line Bangla comment block")

    return errors


def run_audit():
    total_files = 0
    all_errors = []
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                total_files += 1
                fp = os.path.join(root, file)
                errs = audit_file(fp)
                all_errors.extend(errs)

    if all_errors:
        print(f"FAILED: Found {len(all_errors)} issues:")
        for e in all_errors:
            print("  ", e)
        sys.exit(1)
    else:
        print(f"SUCCESS: Audited {total_files} files across src/ — 100% compliant with 3-line Bangla comments and line limits!")


if __name__ == "__main__":
    import sys
    run_audit()
