import praw
import prawcore
import pdb
import time
import re
import os


reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('copypasta+test+dankmemes+me_irl+memes')
alphabet = {
    "a": "卂","b": "乃","c": "匚","d": "刀","e": "乇","f": "下","g": "厶",
    "h": "卄","i": "工","j": "丁","k": "长","l": "乚","m": "从","n": "𠘨",
    "o": "口","p": "尸","q": "㔿","r": "尺","s": "丂","t": "丅","u": "凵",
    "v": "リ","w": "山","x": "乂","y": "丫","z": "乙"
}
call_command="!thicc"


# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

#convert every letter in the given string to the thicc version
def convert(text):
    text = text.lower()
    out = ""
    for char in text:
        if char.isalpha():
            out+=alphabet.get(char)
        else:
            out+=char
    return out

#check if the given string already contains a "thicc character"
def isAlreadyThicc(text):
    for char in text:
        if char in alphabet.values():
            return True
    return False


def thiccify():
    print("-SEARCHING-")
    #go through the stream of comments in the subreddits
    for comment in subreddit.stream.comments():
        #print(comment.body[:6])
        if comment.id not in posts_replied_to:
            if re.search("!thicc", comment.body, re.IGNORECASE):
                #if haven't replied to this comment before and finds the call command
                print("-FOUND COMMENT-")
                #handle differantly if submission or comment
                parent = comment.parent()
                if(type(parent) is type(comment)):
                    text = parent.body
                else:
                    text = parent.title

                if isAlreadyThicc(text):
                    print("-ALREADY IS THICC ")
                    text = convert("ALREADY THICC")
                else:  
                    text = convert(text) 

                print("-REPLYING WITH: "+text)
                try:
                    comment.reply(text)
                    print("-REPLIED-")
                except praw.exceptions.APIException:
                    print("-WAITING 10 MINS FOR RATE LIMIT-")
                    time.sleep(600)
                    comment.reply(text)
                    print("-REPLIED-")
                posts_replied_to.append(comment.id)
                print("-SEARCHING-")    
def write():
    # Write our updated list back to the file
    print("-WRITING TO FILE-")
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
def main():
    print("-STARTED-")
    thiccify()
if __name__ == '__main__':
    try:
        main()
    finally KeyboardInterrupt:
        write()