docker build . -t psb
docker run -it --rm --name psb -p 5001:5000 psb
