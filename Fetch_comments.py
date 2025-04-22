from googleapiclient.discovery import build

# Replace with your API key
API_KEY = "AIzaSyDE1xHah0I0QdAzl6HTxFPC-chT86MRbyA"
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
video_id = "ux9nPrs8zmk"
comments = get_comments(video_id)
print(comments)
