# Author: Carly Palicz
#I pledge my honor that I have abided by the Stevens Honor System
#Homework 3

#  youtube_data.py searches YouTube for videos matching a search term
#  It writes info for each video, up to a specified maximum number, to a .csv file
#  It sorts this information in order of most recently uploaded videos

# to run from terminal window:  
#      python3 youtube_data.py --search_term mysearch --search_max mymaxresults
#  where:  search_term = the term you want to search for;  default = music
#     and  search_max = the maximum number of results;  default = 30

from apiclient.discovery import build      # use build function to create a service object
from operator import itemgetter #added in order to sort list of dictionaries to sort video data by upload date

import argparse    #  need for parsing the arguments in the command line
import csv         #  need since search results will be contained in a .csv file
import unidecode   #  need for processing text fields in the search results


# put your API key into the API_KEY field below, in quotes
API_KEY = "AIzaSyB9gEqelCCsEVKDtMapInHutdUnE4yyqhY"

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

#  function youtube_search retrieves the YouTube records

def youtube_search(options):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    
    search_response = youtube.search().list(q=options.search_term, part="id,snippet", maxResults=options.search_max).execute()
    
    # create a CSV output for results video list, and write the headings line    
    csvFile = open('video_results.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["TITLE","ID","VIEWS","LIKES","DISLIKES","COMMENTS","FAVORITES", "PUBLISHED"])
    
    #added code: made a list of dictionaries for the results so they could be sorted easily by column
    results = []
    

    # search for videos matching search term; write an output line for each
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  
            videoId = search_result["id"]["videoId"]
            #added code: added a column for the publishedAt date of each video
            pub = search_result["snippet"]["publishedAt"]
            #end added code

            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            for video_results in video_response.get("items",[]):
                viewCount = video_results["statistics"]["viewCount"]
                if 'likeCount' not in video_results["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_results["statistics"]["likeCount"]
                if 'dislikeCount' not in video_results["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_results["statistics"]["dislikeCount"]
                if 'commentCount' not in video_results["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_results["statistics"]["commentCount"]
                if 'favoriteCount' not in video_results["statistics"]:
                    favoriteCount = 0
                else:
                    favoriteCount = video_results["statistics"]["favoriteCount"]

            #adds the dictionary item containing the row of info about the video to the list
            results.append({"title": title, "videoId": videoId, "viewCount": viewCount, "likeCount": likeCount, "dislikeCount":dislikeCount, "commentCount":commentCount, "favoriteCount":favoriteCount, "pub":pub})

    #sort the list of dictionaries by the published date so that the newest videos are first on the list
    results_sorted = sorted(results, key=itemgetter('pub'), reverse=True)

    #moved this to outside of the outer for loop so that it can be written after sorted rather than as the searched items are created
    for results in results_sorted:
        csvWriter.writerow([results["title"],results["videoId"],results["viewCount"],results["likeCount"],results["dislikeCount"],results["commentCount"],results["favoriteCount"], results["pub"]])
        
    csvFile.close()
  
# main routine
parser = argparse.ArgumentParser(description='YouTube Search')
parser.add_argument("--search_term", default="music")
parser.add_argument("--search_max", default=30)
args = parser.parse_args()
    
youtube_search(args)
