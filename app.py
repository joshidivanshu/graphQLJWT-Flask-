from flask import Flask
from flask_graphql import GraphQLView
import json
from schema import schema
from database import db_session
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_header_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'divanshu'
app.config["JWT_SECRET_KEY"] = "divanshu"
#  datetime.timedelta & defaults to 15 minutes. 
# app.conifg["JWT_ACCESS_TOKEN_EXPIRES"] 
# datetime.timedelta and defaults to 30 days. 
# Can be set to False to disable expiration.
# app.conifg["JWT_REFRESH_TOKEN_EXPIRES"] 
auth = GraphQLAuth(app)

@app.route('/')
def home():
    return 'home'
  
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)    
    
if __name__ == '__main__':
    app.run(debug=True)