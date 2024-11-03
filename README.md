## Run the API server

```
docker build . -t dicom-app
docker run -p 3000:5000 dicom-app
```

## Connect to the UI in the browser

Browse to localhost:3000 after running API server

## API can also be accessed directly via curl
### list all files

```
curl 0.0.0.0:3000/images
```

### upload a file

- *Caveat: no validation is performed to ensure dicom format.*
- *Caveat: file name MUST end in .dcm*
```
curl -v -X POST 0.0.0.0:3000/images -F "file=@0009.dcm"
```

### get a specific file

```
curl 0.0.0.0:3000/images/im000001.dcm --output myfile.dcm
```

### get a specific file as .png

```
curl 0.0.0.0:3000/images/im000001.dcm?png=true --output myfile.png
```

### delete a file

```
curl -X "DELETE" 0.0.0.0:3000/images/im000001.dcm
```

### get all dicom tags on an image

```
curl 0.0.0.0:3000/images/im000001.dcm/tags
```

### search dicom tags on an image

```
curl 0.0.0.0:3000/images/im000001.dcm/tags?search=0008,0096
curl 0.0.0.0:3000/images/im000001.dcm/tags?search=,0096
curl 0.0.0.0:3000/images/im000001.dcm/tags?search=0008,
curl 0.0.0.0:3000/images/im000001.dcm/tags?search=0008
```

