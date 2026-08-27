# BaseImage
FROM  python:3.11-slim

# Working Directory
WORKDIR /app

# Copy the req
COPY req.txt .

# Install the requiremnts
RUN pip install -r req.txt

# Copy the rest of the code
COPY . .

# Set environment port
ENV PORT=8000

# Expose the port for access
EXPOSE 8000

# Run the app
CMD ["python", "main.py"]

