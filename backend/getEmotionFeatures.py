import cv2
from deepface import DeepFace
import json
import sys
def emotion_func(video_path, target_emotions):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise IOError("Cannot open video file")
    fps = cap.get(cv2.CAP_PROP_FPS)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    emotions_data = {}
    frame_count = 0
    emotion_timestamps = {emotion: [] for emotion in target_emotions}
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'])
            dominant_emotion = result[0]['dominant_emotion']
        except:
            dominant_emotion = "No Face Detected"

        emotions_data[f"frame_{frame_count}"] = dominant_emotion

        # If this frame's emotion is in our target list, store its timestamp
        if dominant_emotion in target_emotions:
            timestamp = frame_count / fps
            emotion_timestamps[dominant_emotion].append(timestamp)
        

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

    cap.release()
    return emotions_data,emotion_timestamps

def consolidate_timestamps(emotion_timestamps):
    """
    Converts timestamps to integer seconds and consolidates consecutive occurrences into ranges.
    
    Args:
        emotion_timestamps (dict): Dictionary with emotions as keys and lists of float timestamps as values
        
    Returns:
        dict: Dictionary with emotions as keys and lists of timestamp ranges as values
    """
    consolidated_results = {}
    
    for emotion, timestamps in emotion_timestamps.items():
        if not timestamps:
            consolidated_results[emotion] = []
            continue
            
        # Convert to integer seconds (remove ms/float part)
        int_timestamps = [int(ts) for ts in timestamps]
        
        # Remove duplicates and sort
        unique_timestamps = sorted(set(int_timestamps))
        
        if not unique_timestamps:
            consolidated_results[emotion] = []
            continue
            
        # Consolidate consecutive timestamps
        ranges = []
        range_start = unique_timestamps[0]
        prev_ts = unique_timestamps[0]
        
        for ts in unique_timestamps[1:]:
            # If there's a gap in consecutive timestamps
            if ts > prev_ts + 1:
                # End the current range
                if range_start == prev_ts:
                    ranges.append(f"{range_start}")  # Single value
                else:
                    ranges.append(f"{range_start}-{prev_ts}")  # Range
                # Start a new range
                range_start = ts
            prev_ts = ts
        
        # Add the last range
        if range_start == prev_ts:
            ranges.append(f"{range_start}")  # Single value
        else:
            ranges.append(f"{range_start}-{prev_ts}")  # Range
            
        consolidated_results[emotion] = ranges
    
    return consolidated_results

def getEmotionFeatures(videoPath):
    #edit this array acc. to what emotions u need
    target_emotions = ["fearful","neutral","No Face Detected"]
    data,emotion_timestamps = emotion_func(videoPath, target_emotions)
    total_frames = len(data)
    emotion_counts = {}

    for emotion in data.values():
        if emotion not in emotion_counts:
            emotion_counts[emotion] = 0
        emotion_counts[emotion] += 1

    emotion_percentages = {emotion: (count / total_frames) * 100 for emotion, count in emotion_counts.items()}
    consolidated_timestamps = consolidate_timestamps(emotion_timestamps)

    final_result = {
        "percentages": emotion_percentages,
        "timestamps": consolidated_timestamps
    }
    return json.dumps(final_result)

#print(getEmotionFeatures(''))
