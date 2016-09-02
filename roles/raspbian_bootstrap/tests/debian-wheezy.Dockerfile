FROM williamyeh/ansible:debian7-onbuild

RUN apt-get update
CMD ["bash", "tests/test-travis.sh"]

