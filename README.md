# Todos

- [ ] Users
  - [ ] User roles
  - [ ] First user created by init will have an admin role

- [ ] Themes
  - [ ] Create
  - [ ] Update
    - [ ] Only themes with parent_id = user.id
  - [ ] Use a new theme

- [ ] Unverified users
  - [ ] Allow unverified user to only call these endpoints:

      Using a middleware would be the best solution by far.

    - [ ] Get Current User
    - [ ] Check if verified
    - [ ] Send verifiation code
      - [ ] Limit calls per day
    - [ ] Verify code
  - [ ] Delete account 24h after creation

- [ ] Email
  - [ ] beautify verify_email.html

- [ ] Admin dashboard
  - [ ] See users, update & deleted etc.

- [ ] Tests
