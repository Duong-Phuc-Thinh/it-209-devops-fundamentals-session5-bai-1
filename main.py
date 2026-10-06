import os
import subprocess
import shutil

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, text=True, capture_output=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def main():
    repo_dir = "demo_reflog_repo"
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir)

    print("=== BƯỚC 1: Khởi tạo Git Repository ===")
    run_cmd("git init", cwd=repo_dir)
    run_cmd('git config user.name "Student"', cwd=repo_dir)
    run_cmd('git config user.email "student@example.com"', cwd=repo_dir)

    print("\n=== BƯỚC 2: Tạo commit ban đầu ===")
    with open(os.path.join(repo_dir, "init.txt"), "w", encoding="utf-8") as f:
        f.write("Initial commit content\n")
    run_cmd("git add .", cwd=repo_dir)
    run_cmd('git commit -m "Initial commit"', cwd=repo_dir)

    print("\n=== BƯỚC 3: Tạo commit quan trọng bị mất sau này ===")
    with open(os.path.join(repo_dir, "feature.txt"), "w", encoding="utf-8") as f:
        f.write("Day la tinh nang quan trong\n")
    run_cmd("git add .", cwd=repo_dir)
    run_cmd('git commit -m "Them tinh nang quan trong"', cwd=repo_dir)

    log_before, _, _ = run_cmd("git log --oneline", cwd=repo_dir)
    print("[Git Log trước khi reset]:")
    print(log_before)

    print("\n=== BƯỚC 4: Giả lập sự cố git reset --hard HEAD~1 ===")
    run_cmd("git reset --hard HEAD~1", cwd=repo_dir)

    log_after, _, _ = run_cmd("git log --oneline", cwd=repo_dir)
    print("[Git Log sau khi bị reset hard (đã mất commit)]:")
    print(log_after)

    print("\n=== BƯỚC 5: Tra cứu lịch sử bằng git reflog ===")
    reflog_out, _, _ = run_cmd("git reflog", cwd=repo_dir)
    print("[Kết quả git reflog]:")
    print(reflog_out)

    target_hash = None
    for line in reflog_out.splitlines():
        if "commit: Them tinh nang quan trong" in line:
            target_hash = line.split()[0]
            break

    print("\n=== BƯỚC 6: Khôi phục commit bằng Reflog ===")
    if target_hash:
        print(f"Tìm thấy commit Hash trong reflog: {target_hash}")
        print(f"Thực thi: git reset --hard {target_hash}")
        run_cmd(f"git reset --hard {target_hash}", cwd=repo_dir)

        log_restored, _, _ = run_cmd("git log --oneline", cwd=repo_dir)
        print("\n[Git Log sau khi khôi phục]:")
        print(log_restored)

        feature_path = os.path.join(repo_dir, "feature.txt")
        if os.path.exists(feature_path):
            with open(feature_path, "r", encoding="utf-8") as f:
                print(f"Nội dung file feature.txt: {f.read().strip()}")
        print("\n=> KẾT QUẢ: Khôi phục commit thành công 100%!")
    else:
        print("Không tìm thấy commit trong reflog.")

if __name__ == "__main__":
    main()
