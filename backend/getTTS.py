import re
from pydub import AudioSegment
import os
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import torch

pipeline = KPipeline(lang_code='a')

        
def split_text_for_tts(text, max_words=29, max_chars=204):
    paragraphs = text.split('\n')
    chunks = []
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
            
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        current_chunk = ""
        current_word_count = 0
        
        for sentence in sentences:
            sentence_words = sentence.split()
            sentence_word_count = len(sentence_words)
            
            if current_word_count + sentence_word_count <= max_words and len(current_chunk + (" " if current_chunk else "") + sentence) <= max_chars:
                current_chunk += " " + sentence if current_chunk else sentence
                current_word_count += sentence_word_count
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
                current_word_count = sentence_word_count
                
                if sentence_word_count > max_words or len(sentence) > max_chars:
                    chunks.append(current_chunk)
                    current_chunk = ""
                    current_word_count = 0
        
        if current_chunk:
            chunks.append(current_chunk)
    
    return chunks

def process_text_to_speech(text, tts_function, output_dir="output_audio", final_output="combined_speech.wav"):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chunks = split_text_for_tts(text)
    
    print(f"Text split into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        word_count = len(chunk.split())
        char_count = len(chunk)
        print(f"Chunk {i}: {word_count} words, {char_count} chars")
        if word_count > 29 or char_count > 204:
            print(f"  WARNING: Chunk {i} exceeds limits ({word_count} words, {char_count} chars)")
    
    audio_files = []
    for i, chunk in enumerate(chunks):
        output_file = os.path.join(output_dir, f"chunk_{i:03d}.wav")
        
        tts_function(chunk, output_file)
        
        audio_files.append(output_file)
    
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        segment = AudioSegment.from_wav(audio_file)
        combined += segment
    
    combined.export(final_output, format="wav")
    
    return final_output

def kokoroTTS(text, output_file):
    print(f"Converting to speech: {text}")
    generator = pipeline(
    text, voice='af_heart', # <= change voice here
    speed=1, split_pattern=r'\n+')
    for i, (gs,ps,audio) in enumerate(generator):
        sf.write(output_file,audio,24000)


def getTTS(text):
    final_audio = process_text_to_speech(text,kokoroTTS)
    print(f"Speech generation complete! Final audio saved to: {final_audio}")

