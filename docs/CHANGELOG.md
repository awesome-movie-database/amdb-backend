# Changelog

## [v0.5.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v0.5.0) (2024-01-29)

### Added

- `User` now can list his `Ratings`

### Changed

- [*Breaking change*] `Rating` now has release date attribute
- Now `Rate movie` endpoint returns `Rating` id

### Fixed

- Bug when `UnrateMovie` endpoint returns error when `Movie` has only one `Rating`

### Echancements

- Added unique constraint for ratings table on user_id and movie_id columns
- Added unique constraint for reviews table on user_id and movie_id columns


## [v0.4.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v0.4.0) (2024-01-27)

### Added

- `User` now can list `Movie` `Reviews`

### Changed

- [*Breaking change*] New WEB API pathes for rate and unrate `Movie`

### Enhancements

- Add endpoint docs for WEB API endpoints
- Update docs for CLI


## [v0.3.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v0.3.0) (2024-01-27)

### Added

- `User` now can review `Movies`
- `User` can get `Review` and list `Movie` `Reviews`

### Changed

- `Movie` now has release date attribute
- [*Breaking change*] Now, to create `Movie`, you must also specify the release date


## [v0.2.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v0.2.0) (2024-01-23)

### Added

- `Superuser` can get `Movie` and list `Movies`

### Fixed

- Bug when a `Movie` is not updating its `Rating` after a `User’s` `Rating`


## [v0.1.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v0.1.0) (2024-01-22)

### Added

- WEB API for `Users`
- `User` can register and login
- `User` can get `Movie` and list `Movies`
- `User` can rate and unrate `Movies`
- `User` can get his rating for `Movie`
- CLI for `Superuser`(admin)
- `Superuser` can create and delete `Movie`
