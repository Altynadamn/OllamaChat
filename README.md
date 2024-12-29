# LlamaChat

LlamaChat is a chat application powered by advanced language models, allowing users to interact with AI models through a simple interface. The app utilizes **Streamlit** for the frontend, integrates **ChromaDB** for persistent data storage, and leverages **Ollama** embeddings to improve response quality. 

## Features

- **Chat with LLMs**: Choose from a variety of AI models to converse with and get responses.
- **Persistent Data Storage**: Saves embeddings in **ChromaDB** for fast retrieval and analysis.
- **Real-time Interaction**: Stream the chatbot's responses in real-time as you type.
- **Customizable Interface**: Users can adjust the model, chat settings, and other preferences.

## Demo

![LlamaChat Demo](assets/demo.gif)

## Technologies Used

- **Streamlit**: For creating an interactive frontend interface.
- **Ollama**: For embedding and generating model responses.
- **ChromaDB**: For persistent storage of embeddings and easy retrieval.
- **Python**: Main programming language for backend logic.

## Installation

### Prerequisites

Before you begin, ensure that you have the following installed:

- Python 3.7+
- `pip` (Python package manager)

### Steps to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LlamaChat.git
   cd LlamaChat
Create a virtual environment (optional but recommended):

`python -m venv venv`

Activate the virtual environment:

- On Windows bash: 
`.\venv\Scripts\activate`

- On macOS/Linux:
`source venv/bin/activate`

- Install the dependencies:
`pip install -r requirements.txt`

- Run the application:
`streamlit run app.py`

Open your browser and go to the URL shown in the terminal, usually http://localhost:8501.


# 🧑‍💻 Usage
Choose a Model: Select which AI model you wish to interact with from the sidebar.
Ask Questions: Type your queries in the chat input field.
Real-time Responses: Enjoy instant AI-generated responses as you chat.
Data Storage: The app stores your interactions in ChromaDB for optimal performance and scalability.

# ⚙️ Configuration
You can customize the following settings:

Model: Pick a model (e.g., Llama 3.2).
Storage: Change the database path if needed (SQLite is used by default via ChromaDB).

Model: Choose which model you want to interact with (e.g., Llama 3.2).
Storage: Change the database location if needed (default is SQLite via ChromaDB).
Contributing
We welcome contributions! If you want to improve this project, please fork the repository and submit a pull request. Here are some guidelines for contributing:

Ensure your code follows PEP 8 standards.
Write tests for new features.
Update the documentation to reflect changes.
License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
We welcome contributions to improve this project! Here's how you can help:

- Fork the Repository: Create a copy of the repository to work on your changes.
- Create a Feature Branch: Use a descriptive name for the branch you're working on.
`git checkout -b feature/your-feature`

-Commit Your Changes: Write clear commit messages.
`git commit -m "Added new feature"`

- Push the Changes:
`git push origin feature/your-feature`



# 💡 Acknowledgments
Special thanks to the incredible tools that made this project possible:

- Streamlit for the user-friendly web interface.
- ChromaDB for persistent, scalable data storage.
- Ollama for high-quality embeddings and language model support.
