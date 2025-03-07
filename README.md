# 📌 YouTube Small Channel Search App

This is a Python app that searches for **small YouTube channels** based on a given query, filtering by subscriber count.

---

## 🚀 Features
- Search for YouTube channels based on a query.
- Filter channels by **minimum and maximum subscribers**.
- Display results including **channel name, ID, subscriber count, and latest video date**.

---

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Create a Virtual Environment (Optional, Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Your API Key
- Create a `.env` file in the project root directory.
- Add your YouTube API key inside `.env`:
  ```
  YOUTUBE_API_KEY=your_actual_api_key_here
  ```
- **Important:** Make sure `.env` is not committed to Git (it's ignored in `.gitignore`).

---

## ▶️ Running the App
To start the app, run:
```bash
streamlit run app.py
```
Then open the **local URL** that appears in the terminal.

---

## 📌 Notes
- If you get **API key errors**, check that your `.env` file is properly set up and that your API key is valid.
- If `os.getenv()` is not reading `.env`, ensure `python-dotenv` is installed and `load_dotenv()` is used in `app.py`.

---

## 📜 License
This project is open-source and free to use. Feel free to contribute! 🚀
