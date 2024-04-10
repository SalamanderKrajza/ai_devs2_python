import asyncio
import aiohttp
import json
import xmltodict

from youtube_transcript_api import YouTubeTranscriptApi

# --------------------------------------------------------------
# Get XML about each video in channel and convert into json
# --------------------------------------------------------------
channels = ["UC_MIaHmSkt9JHNZfQ_gUmrg", "UCTTZqMWBvLsUYqYwKTdjvkw", "UCRHXKLPXE-hYh0biKr2DGIg"]

async def get_videos_data_from_channel(session, channel_id):
    async with session.get(f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}') as response:
        xml = await response.text()
        json_data = xmltodict.parse(xml)
        return create_list_of_videos_from_json_data(json_data, channel_id)

# --------------------------------------------------------------
# Extract data from json_data to list of videos
# --------------------------------------------------------------
def create_list_of_videos_from_json_data(data, channel_id):
    feed = data['feed']
    entries = feed['entry']

    videos = []
    for entry in entries:
        id = entry['yt:videoId']
        title = entry['title']
        url = entry['link']['@href']
        thumbnail = entry['media:group']['media:thumbnail']['@url']
        description = entry['media:group']['media:description']

        video = {
            'id': id,
            'title': title,
            'thumbnail': thumbnail,
            'description': description,
            'url': url,
            'channelId': channel_id,
            'channel': f'https://www.youtube.com/channel/{channel_id}'
        }
        videos.append(video)
    return videos

# --------------------------------------------------------------
# Get video transcription if exists
# --------------------------------------------------------------
async def get_video_transcription(video):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video['id'])
        transcript = transcript_list.find_transcript(['pl']).fetch()
        video['transcription'] = transcript
    except:
        video['transcription'] = ''
    return video


# --------------------------------------------------------------
# Execute the code
# --------------------------------------------------------------
async with aiohttp.ClientSession() as session:
    video_lists = await asyncio.gather(*[get_videos_data_from_channel(session, channel_id) for channel_id in channels])
    
    # Select only 3 first video from each channel
    videos = []
    for channel in video_lists:
        for video in channel[0:3]:
            videos.append(video)

    transcripts = await asyncio.gather(*[get_video_transcription(video) for video in videos])

    print(videos)
    with open('videos.json', 'w') as f:
        json.dump(videos, f, indent=4)

