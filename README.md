# Todos

- [x] Initialisation
  - [x] Create multiple default themes with parent_id = None
  - [x] Create first avatar model
  - [x] Create first account with attribute is_admin = True

- [x] Unverified users
  - [x] Allow unverified user to only call these endpoints:
    - [x] Get Current User
    - [x] Check if verified
    - [x] Send verifiation email
      - [x] Limit calls per day
    - [x] Verify code

      Eaither raise an HTTPException when user is supposed to be verified but isnt
      or try to wrap auth & verify checking in a dependency and use that for most endpoints
  
  - [x] Delete account 24h after creation

      Start a worker that will try to delete this account and its relative models after 24h if not verified

- [x] Themes
  - [x] Change Theme (from pool of defaults + own themes)
  - [ ] ~~Create~~
  - [ ] ~~Update~~

- [ ] Email
  - [ ] beautify verify_email.html

- [ ] Better data validations
  - [ ] Check for same username by comparing lower case to lower case, but save string as given
  - [x] Avatar upload validation

- [ ] Admin dashboard
  - [ ] See accounts & delete accounts

- [ ] Try to find a better way to store/access/update/delete Themes & Avatars

- [ ] Tests

## Ideas

- [ ] Generate favicon based on 'bg' and main 'colors' (letter 'i' in a circle is enough)

## Later

- [ ] Endpoints
  - [ ] /Settings
  - [ ] /notes
