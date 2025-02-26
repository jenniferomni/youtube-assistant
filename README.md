# Multilingual YouTube Video Assistant

This project is a Streamlit-based application that allows users to interact with a custom AI assistant to get information and insights about YouTube videos. The assistant can process video transcripts, detect the language, translate the responses, and provide relevant information based on the user's queries.

## Features

1. **Video Transcript Processing**: The assistant can fetch the transcript for a given YouTube video URL and process it for further analysis.
2. **Language Detection and Handling**: The assistant can detect the original language of the video transcript and provide the user with the option to select their preferred language for the responses.
3. **Multilingual Support**: The assistant can translate the responses to the user's preferred language, making it accessible for a wider audience.
4. **Relevant Information Retrieval**: The assistant can process user queries and provide relevant information based on the video transcript.
5. **Streamlit-based UI**: The application uses the Streamlit framework to provide a user-friendly interface for interacting with the assistant.

## Tools and Libraries Used

The project utilizes a variety of tools and libraries to achieve its functionality:

1. **Python**: The main programming language used for this project.
2. **Streamlit**: A Python library for building interactive web applications. Streamlit is used to create the user interface and handle user interactions.
3. **YouTube Transcript API**: A Python library for fetching video transcripts from YouTube. This API is used to retrieve the transcript for a given video URL.
4. **Deep Translator**: A Python library for translating text between languages. This library is used to translate the assistant's responses to the user's preferred language.
5. **langdetect**: A Python library for detecting the language of a given text. This library is used to detect the original language of the video transcript.
6. **Pydantic**: A Python library for creating data models with type annotations. Pydantic is used to define the data structures for the video information, query results, and other entities.

## Custom Tools and Components

In addition to the external libraries, the project also includes some custom-built tools and components:

1. **CustomAIAssistant**: This is a custom class that encapsulates the core functionality of the AI assistant. It is responsible for tasks such as:
   - Fetching and processing video transcripts
   - Detecting the original language of the transcript
   - Translating the responses to the user's preferred language
   - Providing relevant information based on user queries

2. **VideoInfo**: A Pydantic data model that represents the information about a YouTube video, including the title, description, duration, and detected language.

3. **QueryResult**: A Pydantic data model that encapsulates the assistant's response to a user query, including the answer text and the source references used to generate the response.

4. **Language Code Mapping**: The project includes a dictionary `LANGUAGE_CODES` that maps language codes (e.g., 'en', 'es', 'fr') to their full language names. This is used for providing user-friendly language information.

5. **Streamlit Components**: The application leverages several Streamlit-specific components, such as the `st.chat_message()` and `st.chat_input()` functions, to create a conversational-style interface for the user.

## File Structure

The project has the following file structure:

- `utils/schema.py`: This file contains the data models and the core logic of the AI assistant, including the `CustomAIAssistant` class.
- `index/`: The directory where the video transcripts will be stored. This directory is used to cache the transcripts for faster access and to avoid redundant processing.

## Architecture and Workflow

The Multilingual YouTube Video Assistant follows a specific workflow to provide its functionality:

1. **Video Transcript Processing**: When the user enters a YouTube video URL, the assistant uses the `YouTubeTranscriptApi` to fetch the transcript for the video. The transcript is then processed and stored in the `index/` directory for future use.
2. **Language Detection and Handling**: The assistant detects the original language of the video transcript using the `langdetect` library. If the detected language is not English, the user is prompted to select their preferred language for the responses.
3. **Multilingual Support**: If the user selects a language other than English, the assistant uses the `GoogleTranslator` from the `deep_translator` library to translate the response to the user's preferred language.
4. **Relevant Information Retrieval**: When the user asks a question, the assistant processes the query and searches for relevant information within the video transcript. The response is then provided to the user, along with any relevant source references.

## Future Improvements

1. **Caching and Performance Optimization**: Implement more efficient caching mechanisms to improve the application's performance, especially for repeated queries.
2. **Additional Analytical Features**: Add more advanced analytical features, such as summarization, topic extraction, or sentiment analysis, to provide deeper insights about the video content.
3. **Integrating External Data Sources**: Explore the possibility of integrating additional data sources (e.g., related articles, comments, or video metadata) to enrich the information provided to the user.
4. **Customizable UI**: Allow users to customize the UI layout and appearance to better suit their preferences.
5. **Deployment and Scalability**: Investigate deployment options and scalability strategies to make the application accessible to a wider audience.