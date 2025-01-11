# from app import create_app, db
# import os

# app = create_app()

# with app.app_context():
#     db.create_all()

# if __name__ == '__main__' and not os.getenv('FLASK_RUN_FROM_CLI'):
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


# from app import create_app, db
# import os

# app = create_app()

# with app.app_context():
#     db.create_all()

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

import os
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
