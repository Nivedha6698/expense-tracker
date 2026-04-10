from app import create_app, db
import os

# Read environment (default = dev)
env = os.getenv('APP_ENV', 'dev')

# Create app based on environment
if env == "prod":
    app = create_app("prod")
elif env == "test":
    app = create_app("test")
else:
    app = create_app("dev")

if __name__ == "__main__":
    # Debug only in dev
    debug_mode = True if env == "dev" else False

    app.run(debug=debug_mode, host='0.0.0.0', port=5000)