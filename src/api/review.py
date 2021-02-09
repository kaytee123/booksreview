from bson.objectid import ObjectId
from datetime import datetime
from functools import reduce

from ..shared.result import Result, Error


class Review:
    def __init__(
        self, review_id: str, name: str, rating: int, review: str, created_at: datetime
    ):
        self.id = review_id
        self.name = name
        self.rating = rating
        self.review = review
        self.created_at = created_at

    @staticmethod
    def create(review):
        validity = Review.validate(review)

        if validity["valid"] is False:
            return Result.err(
                Error(validity["message"], "USERINPUT", validity["errors"])
            )

        return Result.ok(
            Review(
                review_id=str(ObjectId(review.get("id"))),
                name=review.get("name"),
                rating=int(review.get("rating")),
                review=review.get("review"),
                created_at=review.get("createdAt", datetime.now()),
            )
        )

    @staticmethod
    def validate(book):
        errors = {}

        if not book.get("name") or book.get("name") == "":
            errors["name"] = "Name is required"

        if (
            not book.get("rating")
            or int(book.get("rating")) > 5
            or int(book.get("rating")) < 0
        ):
            errors["Rating"] = "Rating is required and should be between 0 and 5"

        if not book.get("review") or book.get("review") == "":
            errors["review"] = "Review is required"

        message = ""
        for key in errors:
            message += errors[key] + ". "

        return {
            "valid": True if len(errors) == 0 else False,
            "errors": errors,
            "message": message,
        }


class ReviewList:
    def __init__(self, reviews: [Review]):
        self.__reviews = reviews

    @staticmethod
    def create(reviews: [Review]):
        print(type(reviews))

        return ReviewList(reviews)

    def reviews(self):
        return self.__reviews

    def average_rating(self):
        """
        Get respective rating_point_frequency for each rate points
        Calculate the rating_score for each rating points
        Calculate the total_rating_score of all rating_scores
        Divide the total_rating_score by total_reviews

        rating_score = rating_point * rating_point_frequency eg. 1*a
        total_rating_score = 1*a + 2*b + 3*c + 4*d + 5*e
        average rating = total_rating_score/total_reviews

        """
        if len(self.__reviews) < 1:
            return 0

        reviews = self.__reviews
        rating_scores = [0, 0, 0, 0, 0]

        # Calculating the rating_point_frequency total number of reviews
        # for each rating point expect 0
        for review in reviews:
            if review.rating == 0:
                continue
            rating_scores[review.rating - 1] += 1

        # Calculating rating scores
        for i in range(0, 5):
            rating_scores[i] *= i + 1

        # Calculating total_rating_score
        total_rating_score = reduce(lambda acc, cur: acc + cur, rating_scores)

        # Average rating
        return total_rating_score / len(reviews)


# Mapper
class ReviewMapper:
    @staticmethod
    def to_domain(raw_review):
        return Review(
            review_id=str(ObjectId(raw_review.get("id"))),
            name=raw_review.get("name"),
            rating=raw_review.get("rating"),
            review=raw_review.get("review"),
            created_at=raw_review.get("createdAt"),
        )

    @staticmethod
    def to_dict(review: Review, id_shape="id"):
        return {
            id_shape: review.id,
            "name": review.name,
            "rating": review.rating,
            "review": review.review,
            "createdAt": review.created_at,
        }

    @staticmethod
    def for_update(data: dict):
        update = {}

        if data["name"]:
            update["name"] = data["name"]
        if data["rating"]:
            update["rating"] = data["rating"]
        if data["review"]:
            update["review"] = data["review"]

        return update

    @staticmethod
    def to_persistence(review: Review):
        return ReviewMapper.to_dict(review, id_shape="_id")


class ReviewListMapper:
    @staticmethod
    def to_domain(raw_reviews):
        reviews = [ReviewMapper.to_domain(review) for review in raw_reviews]
        return ReviewList(reviews)

    @staticmethod
    def to_dict(review_list: ReviewList):
        reviews = [ReviewMapper.to_dict(review) for review in review_list.reviews()]
        return {
            "averageRating": review_list.average_rating(),
            "reviews": reviews,
        }

    @staticmethod
    def to_persistence(review_list: ReviewList):
        def map_review(review):
            return ReviewMapper.to_dict(review, id_shape="_id")

        return [map_review(review) for review in review_list.reviews()]
