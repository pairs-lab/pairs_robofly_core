# Local docker registry

You can host your own docker registry that can be used to transmit images to a drone over a local network.
To start the regisry, spin up the compose session in this folder.
The registry is going to be insecure without a proper SSL certificate, therefore, the client needs to treat it in a special way.
Add the following line to `/etc/docker/daemon.json` in the client host operating system to allow pulling from your local registry:

```json
{"insecure-registries":["hostname:5000"]}
```

## Pushing to the local registry

You can tag a local image by prepending the registry as:
```bash
docker tag registry/my_image hostname:5000/my_image
```

Then, push the newly tagged image to the local registry:
```bash
docker push hostname:5000/my_image
```

## Downloading images on the drone

Download the image by calling:
```bash
docker pull hostname:5000/my_image
```

Re-tag the image to the original name
```bash
docker tag hostname:5000/my_image registry/my_image
```
