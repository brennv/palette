heroku login
heroku apps:create palette-dev

# Set environment vars
heroku config:set PALETTE_SECRET=$PALETTE_SECRET
heroku config:set FLASK_APP=/app/autoapp.py

# Set buildpacks
heroku buildpacks:set heroku/python
heroku buildpacks:add --index 2 heroku/nodejs

# Add postgres
heroku addons:create heroku-postgresql:hobby-dev  # sets DATABASE_URL

# Optional addons
heroku addons:create trevor:test
heroku addons:create scheduler:standard
heroku addons:create logentries:le_tryit
heroku addons:create papertrail:choklad

# Deploy, configure, monitor
git push heroku master
heroku run flask db upgrade
heroku logs --tail
