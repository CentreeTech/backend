# centree_backend
Back-end development for the Centree SmartBloc. This back-end handles the data involved in auditory machine learning algorithms. Classifications are stored on the RDS for various types of sounds (sirens, car crashes, etc...). They each refer to a "media", which is usually a wav file, and is stored on an S3. As well, algorithms and models are stored on the system and maintained there.

## There are two servers running:

The main server handles the REST API. The collection is stored in this repository and is called (centree.postman.json) . This API handles everything from adding and removing devices to adding classifications to audio datasets. This server is stored under the "Flask" folder.

The second server is a system that takes in models that require an update. For example, if the Siren model needs a new update, a user can set it's state to "NEEDS_UPDATE", and this server will then pick it up from the database and start building a new model. This server is stored under the "Machine Learning" folder.


## to setup the uwsgi:

open the virtual environment: source ~/centree_backend/Flask/backend_venv/bin/activate

start the uwsgi server: uwsgi --socket 0.0.0.0:5000 --protocol=http -w main:app

