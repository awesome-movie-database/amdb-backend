# Changelog

## [v1.1.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v1.0.0) (2024-03-11)

### Added

- WEB API logout endpoint

### Changed

- [*Breaking change*] Now number of characters in `Movie` title must be more than 1 and less than 128
- [*Breaking change*] Now number of characters in `User` name must be more than 1 and less than 128
- [*Breaking change*] Now `User` name must not contain spaces
- [*Breaking change*] Now number of characters in `Review` title must be more than 5 and less than 128
- [*Breaking change*] Now number of characters in `Review` content must be more than 5 and less than 1024

### Fixed

- Misspell in 'How to run' instruction

### Echancements

- Now Session ID length is 128 characters


## [v1.0.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v1.0.0) (2024-03-10)

### Added

- `User` now can list `detailed reviews`
- `User` now can get `detailed movie`
- `User` now can list his `detailed ratings`
- `User` now can get `non detailed movie`
- `User` now can export his `ratings` in CSV format
- `User` now can request export his `ratings` in CSV format

### Changed

- Now `Create movie` and `Delete movie` don't require permissions
- [*Breaking change*] Now `Review` type is a string
- [*Breaking change*] Removed ability to list `Movies`
- [*Breaking change*] Removed ability to list `Ratings`
- [*Breaking change*] Removed ability to get `Movie`
- [*Breaking change*] Removed ability to get `Review`

### Fixed

- Race condition during rating `Movie` by many `Users` at the same time

### Echancements

- Added permissions table
- Now you can run server and worker using CLI


## [v0.5.0](https://github.com/Awesome-Movie-Database/amdb-backend/releases/tag/v0.5.0) (2024-01-29)

### Added

- `User` now can list his `Ratings`

### Changed

- [*Breaking change*] `Rating` now has release date attribute
- Now `Rate movie` endpoint returns `Rating` id

### Fixed

- Bug when `UnrateMovie` endpoint returns error when `Movie` has only one `Rating`
- Some tests have no 'test' prefix

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
