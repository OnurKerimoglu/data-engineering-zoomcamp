## Question 1. Understanding docker first run 

**Q:** Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint 
`bash`.\
**A:** the command we need is:
`docker run -it --entrypoint=bash python3.12.8`

**Q:** What's the version of `pip` in the image?\
**A:** running the container in interactive mode, and issuing: `pip --version` reveals that the pip version of pip is 24.3.1


