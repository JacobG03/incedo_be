# Todos

- [x] Initialisation
  - [x] Create multiple default themes with parent_id = None
  - [x] Create first avatar model
  - [x] Create first account with attribute is_admin = True

- [ ] Unverified users
  - [ ] Allow unverified user to only call these endpoints:
    - [ ] Get Current User
    - [ ] Check if verified
    - [ ] Send verifiation email
      - [ ] Limit calls per day
    - [ ] Verify code

      Eaither raise an HTTPException when user is supposed to be verified but isnt
      or try to wrap auth & verify checking in a dependency and use that for most endpoints
  
  - [ ] Delete account 24h after creation

      Start a worker that will try to delete this account and its relative models after 24h if not verified

- [ ] Themes
  - [ ] Change Theme (from pool of defaults + own themes)
  - [ ] Create
  - [ ] Update
    - [ ] Only themes with parent_id = user.id

- [ ] Email
  - [ ] beautify verify_email.html

- [ ] Admin dashboard
  - [ ] See users, update & delete etc.

- [ ] Better data validations
  - [ ] Check for same username by comparing lower case to lower case, but save string as given
  - [ ] etc..

- [ ] Tests

## Ideas

- [ ] Generate favicon based on 'bg' and main 'colors' (letter 'i' in a circle is enough)
