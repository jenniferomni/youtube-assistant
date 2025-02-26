#Original main.py 

# import streamlit as st
# import os
# from utils.schema import CustomAIAssistant

# def main():
#     # Set up the Streamlit app title
#     st.title("AI Assistant Chatbot")

#     # Initialize session state for the assistant and chat history
#     if "assistant" not in st.session_state:
#         st.session_state.assistant = None
#         st.session_state.messages = []

#     # Initialize or load the AI assistant
#     if st.session_state.assistant is None:
#         index_path = "./index"  # Directory to store the vector index

#         try:
#             st.session_state.assistant = CustomAIAssistant(index_path=index_path)
#             status_msg = "Loaded existing index." if os.path.exists(index_path) else "Created new index."
#             st.success(status_msg)
#         except Exception as e:
#             st.error(f"Error initializing assistant: {str(e)}")
#             return

#     # Input for the video URL
#     video_url = st.text_input("Enter YouTube Video URL")

#     # Display chat history
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Chat input and response generation
#     if prompt := st.chat_input("Ask your question here..."):
#         # Add user message to chat
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         # Generate and display assistant response
#         with st.chat_message("assistant"):
#             try:
#                 # Ensure a video URL is provided
#                 if not video_url:
#                     st.error("Please enter a valid YouTube video URL.")
#                 else:
#                     # Query the assistant with prompt and video URL
#                     result = st.session_state.assistant.query(prompt, video_url)
#                     st.markdown(result.answer)

#                     # Optional: Display sources if available
#                     if result.source_nodes:
#                         with st.expander("Sources"):
#                             for source in result.source_nodes:
#                                 st.write(source)

#                     # Add assistant response to chat history
#                     st.session_state.messages.append(
#                         {"role": "assistant", "content": result.answer}
#                     )
#             except Exception as e:
#                 error_message = f"Error generating response: {str(e)}"
#                 st.error(error_message)
#                 st.session_state.messages.append(
#                     {"role": "assistant", "content": error_message}
#                 )


# if __name__ == "__main__":
#     main()

#main.py code for Multilingual YouTube Video Assistant


import streamlit as st
from utils.schema import CustomAIAssistant

def initialize_session_state():
    if "assistant" not in st.session_state:
        st.session_state.assistant = CustomAIAssistant()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "video_info" not in st.session_state:
        st.session_state.video_info = None
    if "language_selected" not in st.session_state:
        st.session_state.language_selected = False
    if "current_video_url" not in st.session_state:
        st.session_state.current_video_url = None
    if "transcript_saved" not in st.session_state:
        st.session_state.transcript_saved = False

def display_video_info():
    if st.session_state.video_info:
        st.sidebar.header("Video Information")
        st.sidebar.write(f"Title: {st.session_state.video_info.title}")
        st.sidebar.write(f"Original Language: {st.session_state.video_info.language}")

def main():
    st.title("Multilingual YouTube Video Assistant")

    initialize_session_state()

    video_url = st.text_input("Enter YouTube Video URL")

    # If the video URL has changed, load the transcript for the new video
    if video_url and video_url != st.session_state.current_video_url:
        with st.spinner("Processing video transcript..."):
            # Parse and save transcript
            st.session_state.assistant.load_or_create_transcript(video_url)
            st.session_state.video_info = st.session_state.assistant.get_video_info(video_url)
            st.session_state.current_video_url = video_url
            st.session_state.language_selected = False

            # Save transcript as .txt file
            transcript_text = st.session_state.assistant.get_transcript_text(video_url)  # Pass video_url here
            with open("video_transcript.txt", "w") as file:
                file.write(transcript_text)
            st.session_state.transcript_saved = True
            st.success("Transcript saved as 'video_transcript.txt'")

    display_video_info()

    # Chat functionality
    if prompt := st.chat_input("Ask your question about the video..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                if not video_url:
                    st.error("Please enter a valid YouTube video URL.")
                else:
                    with st.spinner("Generating response..."):
                        result = st.session_state.assistant.query_from_transcript(prompt, "video_transcript.txt")
                        st.markdown(result)

                        st.session_state.messages.append({"role": "assistant", "content": result})
            except Exception as e:
                error_message = f"Error generating response: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

    # Button to clear chat
    if st.button("Clear Chat"):
        st.session_state.messages = []


if __name__ == "__main__":
    main()



#main.py code for presentation

# from utils.schema import CustomAIAssistant
# def main():
#     # Initialize the assistant and set language preferences
#     assistant = CustomAIAssistant(original_language="English", target_language="English")

#     # Prompt for the video URL
#     video_url = input("Please enter the video URL: ")

#     # Load or create the transcript based on the video URL
#     assistant.load_or_create_transcript(video_url)

#     # Provide a summary of the video
#     print("Video Overview:")
#     print(assistant.provide_video_overview())

#     # Enter the query loop
#     while True:
#         query = input("Enter your query (or 'exit' to quit): ")
#         if query.lower() == 'exit':
#             break

#         # Process the query and print the response
#         result = assistant.query(query, video_url=video_url)
#         print(f"Response: {result.answer}")

# if __name__ == "__main__":
#     main()
