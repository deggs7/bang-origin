from bang_server import app, db


@app.after_request
def after_request(response):
    if not app.config['TESTING']:
        db.session.commit()
    db.session.close()
    return response
