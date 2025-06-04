FROM python:3.10

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project files
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
