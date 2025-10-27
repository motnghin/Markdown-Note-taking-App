#Ứng dụng Ghi chú Markdown (Markdown Note-taking App)

Đây là một ứng dụng Flask đơn giản cho phép bạn tải lên các tệp tin Markdown, tự động kiểm tra chính tả (Spell Check) nội dung, và chuyển đổi kết quả sang định dạng HTML để xem trên trình duyệt.

 #Tính năng
Tải lên Tệp tin (File Upload): Tải ghi chú Markdown lên server qua API.

Chuyển đổi Markdown sang HTML: Tự động chuyển đổi file Markdown thành HTML.

Kiểm tra Chính tả (Spell Checking): Kiểm tra và cố gắng sửa các từ sai chính tả trong tài liệu (chỉ hỗ trợ Tiếng Anh).

Cài đặt (Installation)
Dự án này yêu cầu Python 3.x và công cụ quản lý gói pip.

Clone Repository:

Bash

git clone https://github.com/AmanDevelops/python-mini-projects.git
cd python-mini-projects/Markdown\ Note-taking\ App/
Tạo Môi trường Ảo (Virtual Environment):

Bash

python -m venv venv
Kích hoạt Môi trường Ảo:

Trên Windows (PowerShell):

Bash

.\venv\Scripts\activate
Trên Linux/macOS hoặc Windows Git Bash/CMD:

Bash

source venv/bin/activate
(Dấu nhắc lệnh sẽ hiển thị (venv) ở phía trước khi kích hoạt thành công.)

Cài đặt Thư viện Phụ thuộc (Dependencies):

Bash

pip install -r requirements.txt

#CÁCH SỬ DỤNG 

Bước 1: Khởi chạy Flask Server
Bạn cần mở Terminal/CMD thứ nhất và chạy ứng dụng Flask (đảm bảo môi trường (venv) đã được kích hoạt):

Bash

flask run
Giữ cửa sổ Terminal này mở. Server sẽ chạy trên http://127.0.0.1:5000/.

Bước 2: Chuẩn bị File Ghi chú
Tạo file note.md trong thư mục dự án (Markdown Note-taking App/).

QUAN TRỌNG: Để tránh lỗi UnicodeDecodeError, bạn chỉ nên sử dụng tiếng Anh và các ký tự Latinh cơ bản trong file note.md vì ứng dụng không được cấu hình mã hóa UTF-8.

Bước 3: Tải lên File bằng curl
Mở Terminal/CMD thứ hai (cũng kích hoạt (venv)) và sử dụng lệnh curl.exe để gửi file đến API:

Nếu file note.md nằm trong thư mục hiện tại:

Bash

curl.exe -X POST -F "file=@./note.md" http://localhost:5000/api/upload
Lệnh này đã được điều chỉnh để hoạt động ổn định trên Windows PowerShell.

Bước 4: Truy cập Ghi chú đã Xử lý
Server sẽ phản hồi bằng một đối tượng JSON chứa URL:

JSON

{
  "url": "http://localhost:5000/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.html"
}
Mở trình duyệt web của bạn và dán URL đó vào để xem ghi chú đã được chuyển đổi sang HTML và kiểm tra chính tả.
