
# 📋 Danh Sách 10 Câu Hỏi Mẫu Kiểm Thử Pipeline (Gemini + Fish Audio)

Bạn có thể sao chép nhanh các câu hỏi dưới đây vào ô nhập liệu trên Web UI (`http://localhost:7860`) để kiểm tra độ trễ (latency) và khả năng biểu cảm (emotion voice).

---

## 🇻🇳 PHẦN 1: TIẾNG VIỆT (Khuyến nghị chọn giọng: `🇻🇳 Phi Hùng` hoặc `🇻🇳 Nữ VN`)

### 1. Chào hỏi tự nhiên & Test tốc độ nhanh (Latency Benchmark)

- **Prompt:**

```text
Chào bạn! Hãy giới thiệu bản thân trong một câu ngắn thật thân thiện nhé.
```

- **Cài đặt gợi ý:** Giọng: `🇻🇳 Phi Hùng` | Language: `🇻🇳 Tiếng Việt` | Cảm xúc: `😐 Bình thường`
- **Mục tiêu test:** Đo tốc độ phản hồi nhanh nhất (TTFT < 2s, E2E Latency).

---

### 2. Vui vẻ, Hào hứng (Joy & Excitement)

- **Prompt:**

```text
Chúng ta vừa giành giải nhất cuộc thi lập trình rồi! Hãy reo lên chúc mừng mọi người đi!
```

- **Cài đặt gợi ý:** Giọng: `🇻🇳 Phi Hùng` | Language: `🇻🇳 Tiếng Việt` | Cảm xúc: `😄 Vui vẻ / Hào hứng`
- **Mục tiêu test:** Đánh giá cao độ giọng nói, ngữ điệu vui tươi, phấn khởi.

---

### 3. Buồn bã, Trầm lắng (Sadness & Empathy)

- **Prompt:**

```text
Tôi vừa chia tay một người bạn thân đã gắn bó nhiều năm. Hãy an ủi tôi một câu thật xúc động.
```

- **Cài đặt gợi ý:** Giọng: `🇻🇳 Phi Hùng` | Language: `🇻🇳 Tiếng Việt` | Cảm xúc: `😢 Buồn bã / Trầm lắng`
- **Mục tiêu test:** Đánh giá tông giọng trầm, tốc độ đọc chậm rãi, cảm xúc lắng đọng.

---

### 4. Thì thầm, Bí mật (Whispering)

- **Prompt:**

```text
Nói khẽ thôi nhé! Hãy thì thầm cho tôi biết mật mã bí mật để mở cánh cửa kho báu.
```

- **Cài đặt gợi ý:** Giọng: `🇻🇳 Phi Hùng` hoặc `🇻🇳 Nữ VN` | Language: `🇻🇳 Tiếng Việt` | Cảm xúc: `🤫 Thì thầm / Nhẹ nhàng`
- **Mục tiêu test:** Đánh giá khả năng hạ âm lượng, âm gió và hơi thở thì thầm của Fish Audio.

---

### 5. Kịch tính, Khẩn cấp (Dramatic & Urgent)

- **Prompt:**

```text
Cảnh báo khẩn cấp! Tàu vũ trụ đang mất kiểm soát, tất cả phi hành đoàn lập tức vào khoang thoát hiểm trong 5 giây!
```

- **Cài đặt gợi ý:** Giọng: `🇻🇳 Phi Hùng` | Language: `🇻🇳 Tiếng Việt` | Cảm xúc: `🎭 Kịch tính / Hồi hộp`
- **Mục tiêu test:** Đánh giá nhịp điệu dồn dập, gắt gao và độ chân thực trong tình huống khẩn cấp.

---

### 6. Tức giận, Nghiêm khắc (Anger & Strictness)

- **Prompt:**

```text
Dừng lại ngay! Ai cho phép bạn tự ý xâm nhập vào khu vực cấm này hả?
```

- **Cài đặt gợi ý:** Giọng: `🇻🇳 Phi Hùng` | Language: `🇻🇳 Tiếng Việt` | Cảm xúc: `😡 Tức giận / Căng thẳng`
- **Mục tiêu test:** Đánh giá độ gằn giọng và sức nặng của ngữ điệu tiếng Việt.

---

### 7. Thuyết minh khoa học, Rành mạch (Educational & Explanatory)

- **Prompt:**

```text
Hãy giải thích ngắn gọn trong 2 câu vì sao bầu trời lại có màu xanh lam vào ban ngày.
```

- **Cài đặt gợi ý:** Giọng: `🇻🇳 Nữ VN` | Language: `🇻🇳 Tiếng Việt` | Cảm xúc: `😐 Bình thường`
- **Mục tiêu test:** Đánh giá độ rõ ràng, mạch lạc, phát âm các thuật ngữ khoa học.

---

## 🇺🇸 PHẦN 2: TIẾNG ANH (Khuyến nghị chọn giọng: `🇺🇸 Sarah` hoặc `🇺🇸 Energetic Male`)

### 8. English Casual Greeting (So sánh phát âm chuẩn bản xứ)

- **Prompt:**

```text
Hey Sarah! How is your day going, and what exciting things are you up to today?
```

- **Cài đặt gợi ý:** Giọng: `🇺🇸 Sarah` | Language: `🇺🇸 English` | Cảm xúc: `😄 Vui vẻ / Hào hứng`
- **Mục tiêu test:** Đối sánh phát âm tiếng Anh chuẩn bản xứ với phát âm tiếng Việt để thấy rõ sự khác biệt của model nền tảng.

---

### 9. English Inspirational Story (Prosody & Flow)

- **Prompt:**

```text
Give me an inspiring and motivational quote to overcome self-doubt, in two short sentences.
```

- **Cài đặt gợi ý:** Giọng: `🇺🇸 Sarah` | Language: `🇺🇸 English` | Cảm xúc: `😐 Bình thường`
- **Mục tiêu test:** Đánh giá sự mượt mà (smoothness), ngữ điệu nối âm (linking sounds) trong tiếng Anh.

---

### 10. English Dramatic Countdown (High Energy)

- **Prompt:**

```text
3, 2, 1... Ignition! The rocket has successfully cleared the tower and is heading into deep space!
```

- **Cài đặt gợi ý:** Giọng: `🇺🇸 Energetic Male` | Language: `🇺🇸 English` | Cảm xúc: `🎭 Kịch tính / Hồi hộp`
- **Mục tiêu test:** Đánh giá năng lượng đỉnh cao, cách ngắt nhịp và đẩy cảm xúc của giọng nam tiếng Anh.

---

## 💡 Mẹo kiểm thử so sánh nhanh (A/B Testing):

1. **Thử cùng 1 câu tiếng Việt (ví dụ câu số 2):**
   - Lần 1: Chạy với giọng `🇻🇳 Phi Hùng`.
   - Lần 2: Giữ nguyên câu tiếng Việt nhưng chuyển sang giọng `🇺🇸 Sarah`.
   - ➔ Bạn sẽ nghe thấy rõ hiện tượng *Sarah đọc tiếng Việt bằng âm vị tiếng Anh* (accent lơ lớ).
2. **Thử cùng 1 câu tiếng Anh (ví dụ câu số 8):**
   - Chạy với `🇺🇸 Sarah` ➔ Phát âm tiếng Anh tự nhiên 100%.
   - So sánh chỉ số **RTF (Real-Time Factor)** giữa câu tiếng Việt và tiếng Anh (thường dao động từ 0.3 - 0.5).
