# EDW Knowledge Bot

## Aim

This application serves as an interactive question-answering bot for your Engineering Data Warehouse (EDW) manuals. It retrieves relevant content from a vector database built on your PDF manuals and leverages a large language model (LLM) to provide concise, context-aware answers.

## Project Structure

```
EDW Knowledge Bot/
├── data/
│   ├── Manuals/           # Place all PDF manuals here
│   └── ingestion_chroma.py # Script to ingest manuals into Chroma
├── db/                    # Chroma database directory (auto-created)
├── main.py                # Streamlit app entrypoint
├── core.py                # Query runner and LLM integration
├── ingestion_chroma.py    # (alternate path) Data ingestion script
├── README.md              # This README file
└── Pipfile                # Pipenv dependency file
```

## Setup

1. Create a `.env` file in the project root containing your OpenAI API key:

   ```bash
   OPENAI_API_KEY="sk-..."
   ```

   Ensure the key is loaded into the environment (e.g., via `python-dotenv`).
2. Install dependencies and activate the virtual environment using Pipenv:

   ```bash
   pipenv install       # installs dependencies from Pipfile
   pipenv shell         # activates the environment
   ```

## Data Ingestion

Whenever you add or update PDF manuals in `data/Manuals/`, run:

```bash
python data/ingestion_chroma.py
```

This will:

* Load and split all PDFs into text chunks.
* Embed chunks in batches (with rate-limit respect) into a Chroma vector store.
* Auto-persist the vector store in `db/`.

## Running the App

Launch the Streamlit interface with:

```bash
streamlit run main.py
```

Open the displayed local URL in your browser to start chatting with the bot.

## Configuration

* **History reset**: The conversation history resets after 5 turns by default. You can adjust this limit in `main.py`.
* **Chroma parameters**: Modify batch size, chunk size, or embedding model in `data/ingestion_chroma.py`.

## Contributing

Feel free to open issues or pull requests to improve functionality, add new features, or fix bugs.

## License

MIT License. See [LICENSE](LICENSE) for details.
