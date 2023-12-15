from amdb.domain.entities.user import profile as entity
from amdb.infrastructure.database.models.user import profile as model


class ProfileMapper:
    def to_model(
        self,
        *,
        entity: entity.Profile,
    ) -> model.Profile:
        return model.Profile(
            user_id=entity.user_id,
            achievements=entity.achievements,
            movie_ratings=entity.movie_ratings,
            series_episode_ratings=entity.series_episode_ratings,
            approved_reviews=entity.approved_reviews,
            movie_reviews=entity.movie_reviews,
            series_reviews=entity.series_reviews,
            series_season_reviews=entity.series_season_reviews,
            series_episode_reviews=entity.series_episode_reviews,
            given_votes=entity.given_votes,
            gained_votes=entity.gained_votes,
        )

    def to_entity(
        self,
        *,
        model: model.Profile,
    ) -> entity.Profile:
        return entity.Profile(
            user_id=entity.UserId(model.user_id),
            achievements=model.achievements,
            movie_ratings=model.movie_ratings,
            series_episode_ratings=model.series_episode_ratings,
            approved_reviews=model.approved_reviews,
            movie_reviews=model.movie_reviews,
            series_reviews=model.series_reviews,
            series_season_reviews=model.series_season_reviews,
            series_episode_reviews=model.series_episode_reviews,
            given_votes=model.given_votes,
            gained_votes=model.gained_votes,
        )
