import webbrowser

def web_open():
    link_list = [
        "https://www.youtube.com/playlist?list=PLEsfXFp6DpzRMby_cSoWTFw8zaMdTEXgL",
        "https://www.youtube.com/watch?v=c708Nf0cHrs&",
        "https://www.youtube.com/watch?v=c-QsfbznSXI",
        "https://www.youtube.com/watch?v=psB9vBxPqvE&t",
        "https://www.youtube.com/watch?v=GnU7y-9D71Y"
    ]

    for page in link_list:
        webbrowser.open_new_tab(page)