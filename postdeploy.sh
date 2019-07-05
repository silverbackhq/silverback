echo "Running post-deploy scripts from postdeploy.sh"
cp .env.example .env
python manage.py migrate
