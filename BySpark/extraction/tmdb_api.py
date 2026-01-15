# packages
import requests
import time


# define a function to fetch movie data from TMDB API
def fetch_movie_data(api_key, movie_ids):
    """
    Fetches movie data from TMDB API for a list of movie IDs.

    Args:
        api_key (str): TMDB API Key.
        movie_ids (list): List of movie IDs to fetch.

    Returns:
        list: A list of dictionaries containing movie data.
    """
    movies_data = []
    base_url = "https://api.themoviedb.org/3/movie/"

    print(f"Starting extraction for {len(movie_ids)} movies...")
    # Sort movie IDs to ensure consistent order before fetching
    movie_ids = sorted(movie_ids)
    for movie_id in movie_ids:
        try:
            url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
            response = requests.get(url)

            if response.status_code == 200:
                movies_data.append(response.json())
                print(f"Successfully fetched details for movie info: {movie_id}")
            elif response.status_code == 429:
                print("Rate limit reached. Waiting for 10 seconds...")
                time.sleep(10)
                # Retry once
                response = requests.get(url)
                if response.status_code == 200:
                    movies_data.append(response.json())
                    print(f"Successfully fetched details for movie ID: {movie_id} after retry")
                else:
                    print(f"Failed to fetch movie ID {movie_id} after retry: {response.status_code}")
            else:
                print(f"Error fetching movie ID {movie_id}: {response.status_code}")

        except Exception as e:
            print(f"Exception for movie ID {movie_id}: {str(e)}")

    print(f"Extraction complete. Fetched data for: {len(movies_data)} movies.")
    print(f"Failed to fetch data for: {len(movie_ids) - len(movies_data)} movies.")
    return movies_data
