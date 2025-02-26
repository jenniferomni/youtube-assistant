# import os
# from typing import List
# from pydantic import BaseModel, Field
# from youtube_transcript_api import YouTubeTranscriptApi

# # Basic document structure
# class Document(BaseModel):
#     content: str = Field(..., description="The content of the document")
#     metadata: dict = Field(
#         default_factory=dict, description="Document metadata"
#     )

# # Structure for query responses
# class QueryResult(BaseModel):
#     answer: str = Field(..., description="Response to the query")
#     source_nodes: List[str] = Field(
#         ..., description="Source references used"
#     )

# class CustomAIAssistant:
#     def __init__(self, index_path: str = "index"):
#         """
#         Initialize the AI Assistant
#         :param index_path: Path where the transcript content will be stored
#         """
#         self.index_path = index_path
#         self.transcript = None

#     def load_or_create_transcript(self, video_url: str):
#         """Load existing transcript or create new one"""
#         transcript_file = os.path.join(self.index_path, f"{video_url.split('v=')[1]}.txt")
#         if os.path.exists(transcript_file):
#             self.load_transcript(transcript_file)
#         else:
#             self.create_transcript(video_url, transcript_file)

#     def load_transcript(self, transcript_file: str):
#         """Load existing transcript"""
#         with open(transcript_file, "r") as f:
#             self.transcript = f.read()

#     def create_transcript(self, video_url: str, transcript_file: str):
#         """Create new transcript from YouTube video"""
#         try:
#             transcript = YouTubeTranscriptApi.get_transcript(video_url.split("v=")[1])
#             transcript_text = " ".join([segment["text"] for segment in transcript])
#             os.makedirs(self.index_path, exist_ok=True)
#             with open(transcript_file, "w", encoding="utf-8") as f:
#                 f.write(transcript_text)
#             self.transcript = transcript_text
#         except Exception as e:
#             print(f"Error processing video {video_url}: {e}")
#             raise

#     def query(self, query: str, video_url: str) -> QueryResult:
#         """
#         Process a query and return results
#         :param query: User's question or request
#         :param video_url: URL of the YouTube video to analyze
#         :return: QueryResult with answer and sources
#         """
#         self.load_or_create_transcript(video_url)
        
#         if self.transcript:
#             if query.lower() in self.transcript.lower():
#                 answer = f"Based on the video transcript, the query '{query}' is relevant to the video content."
#             else:
#                 answer = "I'm sorry, I couldn't find any relevant information in the video transcript to answer your query."
#         else:
#             answer = "I'm sorry, I was unable to retrieve the video transcript. Please check the URL and try again."
        
#         return QueryResult(
#             answer=answer,
#             source_nodes=[],
#         )
    
# # Example usage
# if __name__ == "__main__":
#     assistant = CustomAIAssistant(
#         index_path="your_index_directory"
#     )
#     video_url = "https://www.youtube.com/watch?v=nCglvjJkU8A&t=71s"
#     result = assistant.query("Summarize this video for me", video_url)
#     print(result.answer)

# Code written for Multilingual YouTube Video Assistant


import os
from typing import List, Tuple
from pydantic import BaseModel, Field
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
import requests
import json
from langdetect import detect
from urllib.parse import parse_qs, urlparse
import streamlit as st
import cohere

LANGUAGE_CODES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'nl': 'Dutch',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ru': 'Russian',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'ur': 'Urdu',
    'te': 'Telugu',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam'
}

class Document(BaseModel):
    content: str = Field(..., description="The content of the document")
    metadata: dict = Field(default_factory=dict, description="Document metadata")

class QueryResult(BaseModel):
    answer: str = Field(..., description="Response to the query")
    source_nodes: List[str] = Field(..., description="Source references used")

class VideoInfo(BaseModel):
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    duration: str = Field(..., description="Video duration")
    language: str = Field(..., description="Detected language")

class CustomAIAssistant:
    def __init__(_self, index_path: str = "index"):
        _self.index_path = index_path
        _self.transcript = None
        _self.translator = GoogleTranslator()
        _self.video_info = None
        _self.original_language = "english"
        _self.target_language = "english"
        _self.cohere_client = cohere.Client(api_key="701G3pd6VNnGrhEmAQmMs8r3SXkvdlD6XBTu4leC")

    def get_language_name(self, lang_code: str) -> str:
        return LANGUAGE_CODES.get(lang_code, lang_code)

    def get_video_info(self, video_id: str) -> VideoInfo:
        try:
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            response = requests.get(oembed_url)
            data = response.json()
            return VideoInfo(
                title=data.get('title', 'Unknown Title'),
                description="Description available after transcript processing",
                duration="Duration available after transcript processing",
                language="Language will be detected from transcript"
            )
        except Exception as e:
            print(f"Error fetching video info: {e}")
            return VideoInfo(title="Unable to fetch title", description="Unable to fetch description", duration="Unknown", language="Unknown")

    def detect_language(self, text: str) -> str:
        try:
            lang_code = detect(text)
            return self.get_language_name(lang_code)
        except Exception as e:
            print(f"Language detection error: {e}")
            return "unknown"

    def translate_text(self, text: str, target_language: str) -> str:
        if target_language.lower() == self.original_language.lower():
            return text
        try:
            return self.translator.translate(text, src_lang=self.original_language, dest_lang=target_language)
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def extract_video_id(self, video_url: str) -> str:
        if 'youtu.be' in video_url:
            return video_url.split('/')[-1]
        query_params = parse_qs(urlparse(video_url).query)
        return query_params.get('v', [''])[0]

    @st.cache_data
    def load_or_create_transcript(_self, video_url: str) -> Tuple[str, str]:
        video_id = _self.extract_video_id(video_url)
        transcript_file = os.path.join(_self.index_path, f"{video_id}.txt")

        if os.path.exists(transcript_file):
            with open(transcript_file, "r", encoding='utf-8') as f:
                _self.transcript = f.read()
                _self.original_language = _self.detect_language(_self.transcript)
        else:
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                try:
                    available_transcripts = transcript_list.find_manually_created_transcript(['en'])
                except:
                    available_transcripts = transcript_list.find_generated_transcript(['en'])
                transcript = available_transcripts.fetch()
                transcript_text = " ".join([segment["text"] for segment in transcript])

                _self.original_language = _self.detect_language(transcript_text)
                _self.transcript = transcript_text

                os.makedirs(_self.index_path, exist_ok=True)
                with open(transcript_file, "w", encoding='utf-8') as f:
                    f.write(transcript_text)

                _self.video_info = _self.get_video_info(video_id)
                _self.video_info.language = _self.original_language
                return transcript_text, _self.original_language

            except Exception as e:
                print(f"Error processing video {video_url}: {e}")
                st.error(f"Error processing video: {e}")
                return "No transcript available", "unknown"

        return _self.transcript, _self.original_language
    def get_transcript_text(_self, video_url: str) -> str:
        """Returns the current transcript text if available, or loads it if not."""
        if not _self.transcript:
            _self.load_or_create_transcript(video_url)
        return _self.transcript or "Transcript not available."


    def query_from_transcript(self, question: str, transcript_path: str) -> str:
        try:
            with open(transcript_path, "r", encoding="utf-8") as f:
                transcript_text = f.read()
                
            if not transcript_text:
                return "Transcript not available for this video."

            prompt = (
                f"Transcript: {transcript_text}\n\n"
                f"Question: {question}\n\n"
                "Answer:"
            )

            response = self.cohere_client.generate(
                model="command", 
                prompt=prompt, 
                max_tokens=150, 
                temperature=0.1
            )
            answer = response.generations[0].text.strip()
            return answer
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response with Cohere."
    
    


# Code Written for Presentation purpose 

# import re
# from typing import List
# from dataclasses import dataclass

# @dataclass
# class QueryResult:
#     answer: str
#     source_nodes: List[str] = None

# class CustomAIAssistant:
#     def __init__(self, original_language="English", target_language="English"):
#         self.original_language = original_language
#         self.target_language = target_language
#         self.transcript = None

#     def load_or_create_transcript(self, video_url: str) -> None:
#         """
#         Simulate loading or creating a transcript based on a video URL.
#         :param video_url: URL of the video for transcript retrieval
#         """
#         if video_url.strip():
#             # Simulated transcript content for demonstration
#             self.transcript = (
#                 "In 1917, Gandhi visited various locations across India, meeting with many leaders and activists. "
#                 "He had significant encounters during this year, including with several prominent individuals in the freedom movement."
#             )
#             print("Transcript loaded successfully.")
#         else:
#             self.transcript = None
#             print("No transcript available for this video.")

#     def provide_video_overview(self) -> str:
#         """
#         Provide a short summary of the transcript.
#         """
#         if not self.transcript:
#             return "No transcript available for this video."
#         return "This is an overview of the video content."

#     def query(self, query: str, video_url: str) -> QueryResult:
#         """
#         Answer a query based on the transcript of the video.
#         :param query: User's question
#         :param video_url: URL of the video to check if transcript exists
#         :return: QueryResult with the answer or default response
#         """
#         if not self.transcript:
#             return QueryResult("I'm sorry, I couldn't find any relevant information in the video transcript to answer your query.")

#         # Basic keyword search for matching answers
#         # Simplify the query and match it to the transcript
#         query_lower = query.lower()
#         if "gandhi" in query_lower and "1917" in query_lower:
#             # Extract a relevant portion of the transcript
#             answer = "In 1917, Gandhi visited various locations across India, meeting with many leaders and activists. He had significant encounters during this year, including with several prominent individuals in the freedom movement."
#         else:
#             answer = f"I'm sorry, I couldn't find any relevant information in the video transcript to answer your query."

#         return QueryResult(answer)

