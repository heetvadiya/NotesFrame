import cv2
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import KMeans

def find_optimal_clusters(feature_vectors):
    distortions = []
    K = range(1, 11)  # Test cluster sizes from 1 to 10
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(feature_vectors)
        distortions.append(kmeans.inertia_)  # Sum of squared distances to closest centroid

    # Select optimal cluster based on the elbow point
    optimal_cluster = 1
    for i in range(1, len(distortions) - 1):
        slope_current = distortions[i] - distortions[i - 1]
        slope_next = distortions[i + 1] - distortions[i]
        if slope_next > slope_current:
            optimal_cluster = i + 1

    return optimal_cluster

def cluster_frames(input_folder, output_final_folder):
    # Load candidate frames
    candidate_frames = []
    for file in os.listdir(input_folder):
        if file.endswith(".jpg"):
            candidate_frames.append(cv2.imread(os.path.join(input_folder, file), cv2.IMREAD_GRAYSCALE))

    # Convert frames to feature vectors using cosine transformation
    feature_vectors = []
    for frame in candidate_frames:
        resized_frame = cv2.resize(frame, (64, 64))
        feature_vector = np.fft.fft2(resized_frame)
        feature_vector = np.abs(feature_vector)
        feature_vectors.append(feature_vector.flatten())

    # Determine optimal number of clusters
    num_clusters = find_optimal_clusters(feature_vectors)

    # Cluster frames using KMeans
    kmeans = KMeans(n_clusters=num_clusters)
    clusters = kmeans.fit_predict(feature_vectors)

    # Create output folder if it doesn't exist
    os.makedirs(output_final_folder, exist_ok=True)

    # Select best frame from each cluster
    cluster_centers = {}
    for cluster_label in np.unique(clusters):
        cluster_frames = [candidate_frames[i] for i, c in enumerate(clusters) if c == cluster_label]
        brightness_scores = [np.mean(frame) for frame in cluster_frames]
        blur_scores = [cv2.Laplacian(frame, cv2.CV_64F).var() for frame in cluster_frames]
        best_frame_index = np.argmax(np.array(brightness_scores) + np.array(blur_scores))
        best_frame = cluster_frames[best_frame_index]
        cluster_centers[cluster_label] = best_frame

    # Save final keyframes
    for label, frame in cluster_centers.items():
        output_path = os.path.join(output_final_folder, f"keyframe_{label}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"Keyframe extracted: {output_path}")

def extract_candidate_frames(video_path, output_temp_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    # Create temp output directory if it doesn't exist
    os.makedirs(output_temp_folder, exist_ok=True)
    
    frame_count = 0
    while True:
        # Capture frame every 5 seconds
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        interval = int(frame_rate) * 5
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count * interval)
        
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save captured frame
        output_path = os.path.join(output_temp_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"Candidate frame extracted: {output_path}")
        
        frame_count += 1
    
    # Release the video capture object
    cap.release()

def cluster_frames(input_folder, output_final_folder):
    # Load candidate frames
    candidate_frames = []
    for file in os.listdir(input_folder):
        if file.endswith(".jpg"):
            candidate_frames.append(cv2.imread(os.path.join(input_folder, file), cv2.IMREAD_GRAYSCALE))
    
    # Convert frames to feature vectors using cosine transformation
    feature_vectors = []
    for frame in candidate_frames:
        resized_frame = cv2.resize(frame, (64, 64))
        feature_vector = np.fft.fft2(resized_frame)
        feature_vector = np.abs(feature_vector)
        feature_vectors.append(feature_vector.flatten())
    
    # Cluster frames using KMeans
    kmeans = KMeans(n_clusters=15)  # You can adjust the number of clusters as per your requirement
    clusters = kmeans.fit_predict(feature_vectors)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_final_folder, exist_ok=True)
    
    # Select best frame from each cluster
    cluster_centers = {}
    for cluster_label in np.unique(clusters):
        cluster_frames = [candidate_frames[i] for i, c in enumerate(clusters) if c == cluster_label]
        brightness_scores = [np.mean(frame) for frame in cluster_frames]
        blur_scores = [cv2.Laplacian(frame, cv2.CV_64F).var() for frame in cluster_frames]
        best_frame_index = np.argmax(np.array(brightness_scores) + np.array(blur_scores))
        best_frame = cluster_frames[best_frame_index]
        cluster_centers[cluster_label] = best_frame
    
    # Save final keyframes
    for label, frame in cluster_centers.items():
        output_path = os.path.join(output_final_folder, f"keyframe_{label}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"Keyframe extracted: {output_path}")

# Example usage:
video_path = "video1.mp4"
output_temp_folder = "temp_frames"
output_final_folder = "final_keyframes"

# Step 1: Extract candidate frames
extract_candidate_frames(video_path, output_temp_folder)

# Step 2: Cluster similar candidate frames
cluster_frames(output_temp_folder, output_final_folder)
