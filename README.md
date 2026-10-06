# Báo Cáo: Khôi phục commit đã mất bằng Git Reflog

## 1. Giới thiệu bài tập
Bài tập yêu cầu tìm hiểu cơ chế lưu trữ lịch sử hoạt động cục bộ của Git thông qua `git reflog`, từ đó khôi phục lại một commit quan trọng vừa bị xóa mất do lỡ thao tác lệnh `git reset --hard HEAD~1` mà không được viết lại code thủ công.

## 2. Các bước thực hiện chi tiết

### Bước 1: Phát hiện sự cố
Sau khi lỡ chạy lệnh:
```bash
git reset --hard HEAD~1
```
Kiểm tra lại bằng `git log --oneline` thấy commit `Them tinh nang quan trong` cùng toàn bộ thay đổi ở file `feature.txt` đã không còn hiển thị.

### Bước 2: Tra cứu nhật ký Reflog
Chạy lệnh để xem lại toàn bộ lịch sử tham chiếu HEAD cục bộ:
```bash
git reflog
```
Kết quả trả về danh sách lịch sử thao tác, ví dụ:
```text
e3a5b2c HEAD@{1}: commit: Them tinh nang quan trong
8f1d2a1 HEAD@{2}: commit: Initial commit
```
Từ đây ta xác định được mã Hash của commit cần khôi phục là `e3a5b2c` (hoặc con trỏ `HEAD@{1}`).

### Bước 3: Khôi phục commit
Sử dụng lệnh `git reset --hard` kết hợp với mã Hash tìm được từ reflog:
```bash
git reset --hard e3a5b2c
```

### Bước 4: Kiểm tra kết quả
- Kiểm tra lịch sử log: `git log --oneline` (commit đã quay trở lại).
- Kiểm tra file mã nguồn: nội dung `feature.txt` đã phục hồi đầy đủ.

---

## 3. Hướng dẫn chạy kịch bản mô phỏng (Python)

File `main.py` được thiết kế để tự động hóa toàn bộ quy trình giả lập từ tạo commit, reset xóa commit, dùng `git reflog` để truy vết và khôi phục tự động.

Yêu cầu: Máy tính đã cài đặt Python 3 và Git.

Lệnh chạy chương trình:
```bash
python main.py
```