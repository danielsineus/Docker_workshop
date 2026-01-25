# Start with slim Python 3.13 image
FROM python:3.13-slim

COPY --from =ghcr.io/astral-sh/uv:latest /uv /bin/
# set the working Directory
WORKDIR /app

# Add virtual environment to PATH to install packages
ENV PATH="/app/venv/bin:$PATH"
 
# cody depency files first 
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]