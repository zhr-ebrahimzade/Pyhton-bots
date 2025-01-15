from typing import Final
from omdb import OMDBClient
import requests
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    InlineQueryHandler,
)

# from omdb_client import search_movie_by_title



BOT_TOKEN: Final =  "************"

OMDB_API_KEY ="cd2ec65e"

client = OMDBClient(apikey=OMDB_API_KEY)
class Movie:
    def __init__(self, title="", year="", imdb_id="", type="", poster=""):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.type = type
        self.poster = poster

    def from_dict(self, movie: dict):
        self.title = movie.get("title", "Untitled")
        self.year = movie.get("year", "Unknown Year")
        self.imdb_id = movie.get("imdb_id", "")
        self.type = movie.get("type", "movie")
        self.poster = movie.get("poster", "")
        return self

def search_movie_by_title(title: str) -> list[Movie]:
    results = client.search(title, media_type="movie")
    movies = []
    for movie in results:
        movie = Movie().from_dict(movie)
        movies.append(movie)
    return movies



async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def search_movie_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    
    if not query:
        await update.inline_query.answer([], cache_time=10, is_personal=True)
        return

    try:
        if " only_poster" in query:
            search_query = query.replace(" only_poster", "").strip()
            movies = search_movie_by_title(search_query)

            results = [
                InlineQueryResultPhoto(
                    id=f"{movie.imdb_id}_{index}",
                    caption=f"{movie.title or 'Untitled'} - {movie.year or 'Unknown Year'}",
                    title=movie.title or "Untitled",
                    thumbnail_url=movie.poster or "",
                    photo_url=movie.poster or "",
                )
                for index, movie in enumerate(movies)
                if movie.imdb_id and movie.poster  # Validate imdb_id and poster
            ]
        else:
            movies = search_movie_by_title(query)

            results = [
                InlineQueryResultArticle(
                    id=f"{movie.imdb_id}_{index}",
                    title=movie.title or "Untitled",
                    input_message_content=InputTextMessageContent(
                        message_text=f"{movie.title or 'Untitled'} - {movie.year or 'Unknown Year'}:\n\nhttps://www.imdb.com/title/{movie.imdb_id}/"
                    ),
                    thumbnail_url=movie.poster or "",
                )
                for index, movie in enumerate(movies)
                if movie.imdb_id and movie.title  # Validate imdb_id and title
            ]

        await update.inline_query.answer(results, cache_time=10, is_personal=True)

    except Exception as e:
        print(f"Error occurred: {e}")
        await update.inline_query.answer([], cache_time=10, is_personal=True)


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))

    # add all your handlers here
    bot.add_handler(InlineQueryHandler(search_movie_inline_query))
    # start bot
    bot.run_polling()
