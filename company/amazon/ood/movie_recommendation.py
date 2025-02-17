from abc import ABC, abstractmethod
from typing import List, Dict


# Define the interface for movie requests
class MovieRequest(ABC):
    @abstractmethod
    def handle_request(self, movie_system: "MovieRecommendationSystem") -> List[str]:
        pass


# Request to get top 10 movies by country
class TopMoviesByCountryRequest(MovieRequest):
    def __init__(self, country: str):
        self.country = country

    def handle_request(self, movie_system: "MovieRecommendationSystem") -> List[str]:
        return movie_system.get_top_movies_by_country(self.country)


# Request to get top 10 recommended movies for a user
class TopRecommendedMoviesRequest(MovieRequest):
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_request(self, movie_system: "MovieRecommendationSystem") -> List[str]:
        return movie_system.get_recommended_movies(self.user_id)


# Movie recommendation system class
class MovieRecommendationSystem:
    def __init__(self):
        # Example data: movie rankings by country and user preferences
        self.movies_by_country: Dict[str, List[str]] = {
            "USA": ["Movie A"],
            "India": ["Movie X"],
        }
        self.user_recommendations: Dict[str, List[str]] = {
            "user1": ["Rec Movie 1"],
            "user2": ["Rec Movie A"],
        }
        self.user_watch_history: Dict[str, set] = {
            "user1": {"Movie A", "Movie B"},
            "user2": {"Movie X", "Movie Y"},
        }

    def get_top_movies_by_country(self, country: str) -> List[str]:
        return self.movies_by_country.get(country, [])[:10]

    def get_recommended_movies(self, user_id: str) -> List[str]:
        recommendations = self.user_recommendations.get(user_id, [])
        watched = self.user_watch_history.get(user_id, set())
        return [movie for movie in recommendations if movie not in watched]

    def add_to_watch_history(self, user_id: str, movie: str):
        if user_id not in self.user_watch_history:
            self.user_watch_history[user_id] = set()
        self.user_watch_history[user_id].add(movie)

    def process_request(self, request: MovieRequest) -> List[str]:
        return request.handle_request(self)


# Example usage
if __name__ == "__main__":
    movie_system = MovieRecommendationSystem()

    # Create requests
    request1 = TopMoviesByCountryRequest("USA")
    request2 = TopRecommendedMoviesRequest("user1")

    # Process requests
    top_movies_in_usa = movie_system.process_request(request1)
    recommended_movies_for_user1 = movie_system.process_request(request2)

    print("Top Movies in USA:", top_movies_in_usa)
    print("Recommended Movies for User1:", recommended_movies_for_user1)
