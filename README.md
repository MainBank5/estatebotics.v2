# EstateBotics v2

EstateBotics v2 is a real estate chatbot powered by FastAPI and the OnOffice API, designed to help users search and retrieve property listings through a conversational interface. The chatbot is integrated with OpenAI's GPT to provide an intuitive and seamless user experience.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Features
- Fast and scalable backend powered by **FastAPI**.
- **OnOffice API** integration to fetch and search real estate properties.
- Conversational chatbot interface powered by **OpenAI GPT**.
- Secure environment with **API token and HMAC** for authenticating API requests.
- Extensible design allowing easy addition of new features and integrations.

## Tech Stack
- **Backend**: FastAPI, Python
- **Frontend**: React.js
- **Database**: OnOffice API (for property data), PostgreSQL
- **Other**: OpenAI GPT for chatbot responses, HMAC authentication, GitHub for version control

## Getting Started

Follow the steps below to set up the project on your local machine:

### Prerequisites
- Python 3.x
- Git
- A GitHub account
- OnOffice API credentials (API token and secret)
- OpenAI API key

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MainBank5/estatebotics.v2.git
    cd estatebotics.v2
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root of the project and add your API credentials as shown in the example below.

    `.env` Example:

    ```env
    ONOFFICE_API_TOKEN=your_onoffice_api_token
    ONOFFICE_API_SECRET=your_onoffice_api_secret
    OPENAI_API_KEY=your_openai_api_key
    ```

5. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

   Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the automatically generated FastAPI documentation.

## Project Structure

```estatebotics.v2/ ├── .venv/ # Virtual environment (not included in Git) ├── .env # Environment variables (not included in Git) ├── pycache/ # Compiled Python files (not included in Git) ├── main.py # Main FastAPI application entry point ├── chatbot_service.py # Chatbot service logic (integrates with OpenAI GPT) ├── onoffice_service.py # OnOffice API integration logic ├── requirements.txt # Project dependencies ├── .gitignore # Git ignore file └── README.md # Project documentation```


## API Endpoints

Here are the core endpoints for interacting with the chatbot and OnOffice API.

- **GET /properties**

  Fetches all properties from the OnOffice API based on filters (e.g., location, price).

- **POST /chatbot**

  Interacts with the chatbot to respond to user queries.

  **Body:**

    ```json
    {
      "message": "Search for properties in Berlin"
    }
    ```

- **GET /docs**

  Interactive API documentation using FastAPI's automatic documentation system.

## Environment Variables

- `ONOFFICE_API_TOKEN`: Your OnOffice API token for authentication.
- `ONOFFICE_API_SECRET`: Your OnOffice API secret for HMAC calculation.
- `OPENAI_API_KEY`: Your OpenAI API key for the chatbot integration.

Make sure to create a `.env` file in your project root and store these credentials securely.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or support, feel free to contact me at eliudkaruga97@gmail.com.

