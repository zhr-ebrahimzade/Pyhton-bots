from omdb import OMDBClient

OMDB_API_KEY ="cd2ec65e"

client = OMDBClient(apikey=OMDB_API_KEY)

class Movie(object):
    def __init__(
        self,
        title: str = "",
        year: str = "",
        imdb_id: str = "",
        type: str = "",
        poster: str = "",
    ):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.type = type
        self.poster = poster


# class Movie:
#     def __init__(self, title="", year="", imdb_id="", type="", poster=""):
#         self.title = title
#         self.year = year
#         self.imdb_id = imdb_id
#         self.type = type
#         self.poster = poster

#     def from_dict(self, movie: dict):
#         self.title = movie.get("title", "Untitled")
#         self.year = movie.get("year", "Unknown Year")
#         self.imdb_id = movie.get("imdb_id", "")
#         self.type = movie.get("type", "movie")
#         self.poster = movie.get("poster", "")
#         return self

def search_movie_by_title(title: str) -> list[Movie]:
    results = client.search(title, media_type="movie")
    movies = []
    for movie in results:
        movie = Movie().from_dict(movie)
        movies.append(movie)
    return movies
