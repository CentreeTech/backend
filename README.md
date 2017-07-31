# centree_backend
Back-end development for the Centree SmartBloc.


to setup the uwsgi:

open the virtual environment: source ~/centree_backend/Flask/backend_venv/bin/activate

start the uwsgi server: uwsgi --socket 0.0.0.0:5000 --protocol=http -w main:app
