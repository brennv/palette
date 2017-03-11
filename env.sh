#!/bin/sh
# Set environment variables
export FLASK_DEBUG=1  # 0 for prod, 1 for dev
echo "FLASK_DEBUG: $FLASK_DEBUG"
export FLASK_APP="$(pwd)/autoapp.py"
echo "FLASK_APP: $FLASK_APP"

# Create keys.sh if not found
[ ! -f "keys.sh" ] && cat > keys.sh <<- EOM
export PALETTE_SECRET="super-secret"  # TODO change
export DATABASE_URL="postgresql://postgres:postgres@localhost/postgres"
# export DATABASE_URL="sqlite:///$(pwd)/dev.db"
EOM

# Set environment secrets
source keys.sh

# Install virtual environment if not found
[ ! -d "env" ] && virtualenv -p python env

# Activate the virtual environment
source env/bin/activate

# Install requirements for dev or prod
[ $FLASK_DEBUG = 1 ] && pip install -r requirements/dev.txt
[ $FLASK_DEBUG = 0 ] && pip install -r requirements/prod.txt

# Install abd bundle assets
bower install
flask assets build

# Create db/ & migrations/ if not found
# [ ! -d "migrations" ] && mkdir db
# docker run -td -p 5432:5432 -v $(pwd)/db:/var/lib/postgresql/data postgres:9.6.1
# [ ! -d "migrations" ] && flask db init  # && \
#   yes | cp -rf hacks/env.py migrations/env.py  # for batch patch

# Sync models with db
# flask db migrate
# flask db upgrade

# Load data if found
# [ -f "data.py" ] && python -c "import data; data.load()"

# heroku login
# heroku apps:create palette-dev
# heroku config:set PALETTE_SECRET=$PALETTE_SECRET
# heroku config:set FLASK_APP=/app/autoapp.py
# heroku buildpacks:set heroku/python
# heroku buildpacks:add --index 2 heroku/nodejs
# heroku addons:create heroku-postgresql:hobby-dev  # sets DATABASE_URL
  # heroku addons:create trevor:test
  # heroku addons:create scheduler:standard
  # heroku addons:create logentries:le_tryit
# git push heroku master
# heroku logs
# heroku run flask db upgrade
