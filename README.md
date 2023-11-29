# EDW OM A bot

shift&cmd P to select the python interpretor for the applicable environment

pipenv shell to create&activate environment
exit to exit environment
pipenv install to install all modules in pipfile
streamlit run main.py , ctrl c to stop


try:
from langchain.text_splitter import LatexTextSplitter
latex_text = "..."
latex_splitter = LatexTextSplitter(chunk_size=100, chunk_overlap=0)
docs = latex_splitter.create_documents([latex_text])

Selecting a Range of Chunk Sizes - Once your data is preprocessed, the next step is to choose a range of potential chunk sizes to test. As mentioned previously, the choice should take into account the nature of the content (e.g., short messages or lengthy documents), the embedding model you’ll use, and its capabilities (e.g., token limits). The objective is to find a balance between preserving context and maintaining accuracy. Start by exploring a variety of chunk sizes, including smaller chunks (e.g., 128 or 256 tokens) for capturing more granular semantic information and larger chunks (e.g., 512 or 1024 tokens) for retaining more context.

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

https://betterprogramming.pub/building-a-multi-document-reader-and-chatbot-with-langchain-and-chatgpt-d1864d47e339

https://www.activeloop.ai/resources/data-chad-an-ai-app-with-lang-chain-deep-lake-to-chat-with-any-data/

https://www.activeloop.ai/resources/ultimate-guide-to-lang-chain-deep-lake-build-chat-gpt-to-answer-questions-on-your-financial-data/

https://betterprogramming.pub/youtube-chatbot-using-langchain-and-openai-f8faa8f34929
