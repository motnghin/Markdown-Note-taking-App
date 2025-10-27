import re
import uuid
import os
import markdown
from flask import Flask, request
from spellchecker import SpellChecker

# ----------------------------------------------------
# 1. Khởi tạo Flask và tạo thư mục
# ----------------------------------------------------

app = Flask(__name__)
# Tạo thư mục 'uploads' nếu chưa tồn tại
os.makedirs('uploads', exist_ok=True)


@app.route("/api/upload", methods=["POST"])
def handle_upload():
    # 2. Khởi tạo SpellChecker
    spell = SpellChecker()
    file = request.files.get("file") # Dùng .get để tránh lỗi nếu không có file
    
    # Kiểm tra xem có file được tải lên không
    if not file:
        return {"success": False, "message": "No file uploaded"}, 400

    # 3. Tạo ID duy nhất cho file
    file_id = str(uuid.uuid4())
    markdown_filepath = os.path.join("uploads", file_id + ".md") # Lưu tạm file Markdown
    html_filepath = os.path.join("uploads", file_id + ".html") # Đường dẫn file HTML cuối cùng

    # 4. Lưu file Markdown tạm thời
    try:
        file.save(markdown_filepath)
    except Exception as e:
        return {"success": False, "message": f"Error saving file: {e}"}, 500

    # 5. Đọc file, Kiểm tra chính tả và Chuyển đổi (Đã sửa lỗi Encoding và Logic)
    try:
        # Sửa lỗi: Đọc từ file Markdown đã lưu, với encoding UTF-8
        with open(markdown_filepath, 'r', encoding='utf-8') as f:
            data = f.read()

        # Kiểm tra chính tả và sửa lỗi
        # Loại bỏ các từ trong ngoặc đơn khỏi việc kiểm tra chính tả (như URL)
        words = re.findall(r"(?<!\()\b\w+\b(?![^()]*\))", data)
        misspelled = spell.unknown(words)

        for word in misspelled:
            correction = spell.correction(word)
            
            # Sửa lỗi logic: kiểm tra 'https' không nên bị bỏ qua
            # if word in ('https'): continue # Câu lệnh này là vô nghĩa và có thể gây lỗi

            if correction is not None:
                # Sửa lỗi: Chỉ thay thế từ sai chính tả bằng từ sửa nếu nó không phải từ gốc
                if correction.lower() != word.lower():
                    data = re.sub(rf"\b{re.escape(word)}\b", correction, data)

        # Chuyển Markdown thành HTML
        html = markdown.markdown(data)

        # Ghi kết quả HTML vào file .html
        with open(html_filepath, "w", encoding='utf-8') as f: # Dùng encoding UTF-8 khi ghi file HTML
            f.write(html)

        # Xóa file Markdown gốc sau khi xử lý xong (Tùy chọn, để giữ cho thư mục uploads sạch sẽ)
        os.remove(markdown_filepath) 

        return {"url": "http://localhost:5000/" + file_id + ".html"}

    except UnicodeDecodeError:
        return {"success": False, "message": "Encoding Error: Please ensure your note.md is saved with UTF-8 encoding."}, 500
    except Exception as e:
        return {"success": False, "message": f"Processing Error: {e}"}, 500


@app.route("/<file_id>")
def handle_file(file_id):
    # Lấy file HTML đã chuyển đổi
    file_path = os.path.join("uploads", file_id)
    try:
        # Sửa lỗi: Thêm encoding='utf-8' khi đọc file HTML
        with open(file_path, "r", encoding='utf-8') as f:
            # Trả về nội dung HTML và mã 200 OK
            return f.read(), 200
    except FileNotFoundError:
        # Nếu file không tồn tại
        return "404 Not Found", 404
    except Exception:
        # Các lỗi khác
        return "Error loading file", 500

if __name__ == '__main__':
    app.run(debug=True)