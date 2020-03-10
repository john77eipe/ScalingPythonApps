- Clone the repository and open terminal from project directory.
- Create a virtual environment for installing dependencies. A new directory gets created.
`python3 -m venv .myenv`
- Activate it using the source command. Notice the environment name (.myenv) in terminal after executing this.
`source .myenv/bin/activate`
- Navigate into the cloned folder
- Install the requirements using pip command.
`pip install -r requirements.txt`
- Make sure RabbitMQ server is running
- Run one or more workers
`celery worker -A server.celery --loglevel=INFO --concurrency=1`
- Run the server
`python server.py`