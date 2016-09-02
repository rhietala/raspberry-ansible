FROM williamyeh/ansible:debian8-onbuild

RUN apt-get update
CMD ["bash", "tests/test-travis.sh"]

