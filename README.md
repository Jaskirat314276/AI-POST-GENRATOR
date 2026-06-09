<div align="center">

# ✨ LinkedIn Post Generator

**Write on-brand LinkedIn posts in seconds — in your favorite influencer's voice.**

Pick a topic, length, and language. The app pulls real posts on that topic, feeds them to an LLM as few-shot examples, and generates a new post that matches the writing style.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036)
![License](https://img.shields.io/badge/License-MIT-22c55e)

<img src="resources/tool.jpg" width="780" alt="App screenshot" />

</div>

---

## 🚀 What it does

Feed the tool a pile of LinkedIn posts from an influencer. It will:

1. **Extract** the topic, language, and length of every post.
2. **Unify** noisy tags (e.g. *Jobseekers*, *Job Hunting* → **Job Search**).
3. **Generate** a brand-new post that mirrors the writer's tone, by using similar past posts as few-shot examples.

Perfect for ghostwriters, personal-brand builders, and anyone tired of staring at an empty LinkedIn composer.

## 🧠 How it works

```
Raw posts ──► Metadata extraction ──► Tag unification ──► processed_posts.json
                                                                  │
                                                                  ▼
        Pick topic + length + language ──► Few-shot retrieval ──► LLM ──► New post
```

<img src="resources/architecture.jpg" width="780" alt="Architecture diagram" />

- **Stage 1 — Preprocess (`preprocess.py`):** For each raw post, an LLM extracts `line_count`, `language` (English / Hinglish), and `tags`. A second LLM pass merges similar tags into a clean taxonomy.
- **Stage 2 — Generate (`post_generator.py`):** Given a topic + length + language, the app retrieves up to two matching posts from `data/processed_posts.json` and includes them in the prompt as style examples.

## 🛠 Tech stack

| Layer        | Tool                                            |
| ------------ | ----------------------------------------------- |
| UI           | Streamlit (custom glassmorphism CSS)            |
| Orchestration| LangChain                                       |
| LLM          | Llama 3.3 70B Versatile via Groq                |
| Data         | pandas + JSON                                   |
| Config       | python-dotenv                                   |

## ⚡ Quick start

### 1. Clone and install

```bash
git clone <your-fork-url>
cd AI-POST-GENRATOR
pip install -r requirements.txt
```

### 2. Add your Groq API key

Grab one free from [console.groq.com/keys](https://console.groq.com/keys), then create a `.env` in the project root:

```env
GROQ_API_KEY=gsk_your_key_here
```

### 3. Run it

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) and start generating.

## 🎨 Personalize the writing style

Want posts in *your* voice? Replace the examples in `data/raw_posts.json` with your own LinkedIn posts (same JSON shape — just a `text` field per post is enough) and run:

```bash
python preprocess.py
```

This rebuilds `data/processed_posts.json` with fresh metadata and tags. Restart the app and the topic dropdown will reflect your content.

## 📁 Project structure

```
.
├── main.py                  # Streamlit app + UI
├── post_generator.py        # Prompt construction & generation
├── few_shot.py              # Filters past posts for few-shot examples
├── preprocess.py            # Tag + metadata extraction pipeline
├── llm_helper.py            # Groq + Llama 3.3 70B client
├── data/
│   ├── raw_posts.json       # Source posts (replace with your own)
│   └── processed_posts.json # Enriched with line_count, language, tags
├── resources/               # Screenshots
└── requirements.txt
```

## ⚙️ Configuration knobs

| What            | Where                                            |
| --------------- | ------------------------------------------------ |
| Swap the model  | `llm_helper.py` → `model_name`                   |
| Length buckets  | `few_shot.py` → `categorize_length()`            |
| # of examples   | `post_generator.py` → `if i == 1: break`         |
| Theme & CSS     | `main.py` → `CUSTOM_CSS`                         |

## 🤝 Contributing

PRs welcome — issues even more so. Things on the wish list:
- Multi-LLM support (OpenAI, Anthropic, local Ollama)
- Image-prompt generation alongside the post
- One-click "post to LinkedIn" via the official API

## 📄 License

MIT — see below. Built on top of the open-source [Codebasics](https://github.com/codebasics) project; commercial use of the original codebase requires permission from the original author.

> Copyright © Codebasics Inc. All rights reserved. Attribution must be given in all copies or substantial portions of the software.
