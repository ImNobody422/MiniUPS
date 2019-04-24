# ERSS-project-ld190-kw284

## How to Run
- change world server address:
   - Run `cd erss-project-ld190-kw284/ups_server`
   - Run `emacs ups_server.py`
   - change the value of `world_host`
- Run `cd erss-project-ld190-kw284`
- Run `sudo docker-compose build`
- Run `sudo docker-compose up`

## Possible Problems
- database migration fails:
   - delete all unrelated tabls in the docker database
