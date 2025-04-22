from googleapiclient.discovery import build

# Replace with your API key
API_KEY = "XXXXXXXXXXXXXXXX"
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    while request:
        response = request.execute()
        for item in response["items"]:
            comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
        request = youtube.commentThreads().list_next(request, response)
    return comments

#fetch comments for a specific video
video_id = "THE VIDEO ID YOU WANT TO ANALYZE"
comments = get_comments(video_id)
print(comments)
