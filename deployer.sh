set -e

echo "Deploying application ..."

set -e

echo "Deploying application ..."

# Enter maintenance mode

# Update codebase
git reset --hard
git pull origin main
# Exit maintenance mode

sudo supervisorctl reload 

echo "Application deployed right!"
