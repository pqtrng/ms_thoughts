# ms_thoughts

Simple micro-services with Flask

|        | Endpoint                | Requires Authentication | Returns                                   |
|--------|-------------------------|-------------------------|-------------------------------------------|
| GET    | /api/me/thoughts/       | Yes                     | List of thought of users                  |
| POST   | /api/me/thouhgts/       | Yes                     | The newly created thought                 |
| GET    | /api/thouhgts/          | No                      | List of all thoughts                      |
| GET    | /api/thouhgts/X         | No                      | The thought with ID X                     |
| GET    | /api/thoughts/?search=X | No                      | Searches all the thoughts that contains X |
| DELETE | /admin/thoughts/X       | No                      | Deletes thought with ID X                 |
