# Todos

- [x] Initialisation
  - [x] Create multiple default themes with parent_id = None
  - [x] Create first avatar model
  - [x] Create first account with attribute is_admin = True

- [ ] Unverified users
  - [ ] Allow unverified user to only call these endpoints:

      Using a middleware would be the best solution by far.

    - [ ] Get Current User
    - [ ] Check if verified
    - [ ] Send verifiation code
      - [ ] Limit calls per day
    - [ ] Verify code
  - [ ] Delete account 24h after creation

- [ ] Themes
  - [ ] Change Theme (from pool of defaults + own themes)
  - [ ] Create
  - [ ] Update
    - [ ] Only themes with parent_id = user.id

- [ ] Email
  - [ ] beautify verify_email.html

- [ ] Admin dashboard
  - [ ] See users, update & deleted etc.

- [ ] Better data validations
  - [ ] Check for same username by comparing lower case to lower case, but save string as given
  - [ ] etc..

- [ ] Tests

## Ideas

- [ ] Generate favicon based on 'bg' and main 'colors' (letter 'i' in a circle is enough)
