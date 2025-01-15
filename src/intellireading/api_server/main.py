
def entrypoint():
    import uvicorn
    from intellireading.api_server.app import app
    uvicorn.run(app, host="0.0.0.0", port=80) #noqa S104

if __name__ == "__main__":
    entrypoint()
