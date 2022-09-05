import random
import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/chart/top"
title_url = "https://www.imdb.com/title/"

def get_genre(movie_url):
    response = requests.get(movie_url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    content = soup.select("div.ipc-page-content-container span.ipc-chip__text")
    
    genres = [tag.text for tag in content]
    return genres[:-1] #return without last index ("back to top" filler)

def main():
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    movietags = soup.select("td.titleColumn")
    inner_movietags = soup.select("td.titleColumn a")
    rating_tags = soup.select("td.posterColumn span[name=ir]")
    title_ids = soup.select("td.ratingColumn div.seen-widget")    

    def get_year(movie_tag):
        moviesplit = movie_tag.text.split()
        year = moviesplit[-1]
        return year

    years = [get_year(tag) for tag in movietags]
    actors_list = [tag["title"] for tag in inner_movietags]
    titles = [tag.text for tag in inner_movietags]
    ratings = [float(tag["data-value"]) for tag in rating_tags]
    n_movies = len(titles)

    while(True):
        idx = random.randrange(0, n_movies)
        title_id = title_ids[idx]["data-titleid"]
        movie_url = title_url + title_id

        print(f"{titles[idx]} {years[idx]}\nRating: {ratings[idx]:.1f}\nStarring: {actors_list[idx]}\nGenres: {get_genre(movie_url)}\nUrl: {movie_url}\n")

        user_input = input("Do you want another movie suggestion (y/[n])?")
        if user_input != "y":
            break

if __name__ == "__main__":
    main()
