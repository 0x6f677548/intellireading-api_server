def entrypoint():
    import uvicorn
    from intellireading.api_server.app import app

    # this entrypoint should be used for dev purposes only
    # for production, make sure you use a proper server
    # and bind only to the appropriate interfaces
    uvicorn.run(app, host="0.0.0.0", port=8081)  # noqa S104


if __name__ == "__main__":
    entrypoint()
