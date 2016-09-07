# run development server
if __name__ == '__main__':
    from app import wsgi_app # defined in app/__init__.py
    # Configurations
    wsgi_app.config.from_object('config')
    wsgi_app.run(debug=True, host='127.1.33.7', port=3000)
