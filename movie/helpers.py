import re



def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title


