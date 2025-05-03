# GradProject

## Description
This project is part of the GradProject software application, built with Flask. It provides various functionalities for users and is intended for academic purposes.

---

## Before Downloading the Project
Before downloading this project, you should have **Ollama** installed.

[Download Ollama](https://ollama.com/)

After installing it, run the following command in CMD:
`ollama run deepseek-r1:7b`

Make sure Ollama is running while using the project.

---

## Installation

If you are downloading this project for the first time, follow these steps:

### 1. Clone the Repository:

   Clone the project repository to your local machine:

   `git clone https://github.com/BlackFoxT/GradProject`
   `cd GradProject`

### 2. Prepare the project environment:

   Creating new environment for project:

   `python -m venv venv`

   Activate the environment:

   ##### Windows
   `venv\scripts\activate`

   ##### Linux
   `source venv/bin/activate`

   Install the dependencies from requirements.txt:

   `pip install -r requirements.txt`

### 3. Start the project

   You should open the project in the environment:

   `python server.py`

---

## Git Setup Instructions

Follow these instructions for cloning, setting up the remote repository, and handling local changes.

### 1. First Cloning Operation

If this is your first time using the repository, clone it to create a local copy:

`git clone https://github.com/BlackFoxT/GradProject`

After cloning, you do **not** need to use `git remote add origin` again. It is only necessary the first time to link your local repository to the remote repository.

### 2. Setting Up the Remote for Pulling

If you already have a local repository and want to link it to the remote repository, follow these steps:

#### 2.1. Commit Your Changes Before Pulling

If you have local changes that you want to keep before pulling the latest updates from the remote repository, follow these steps:

- **Link your local repository to the remote repository** (this only needs to be done once):

  `git remote add origin https://github.com/BlackFoxT/GradProject`

- **Set the default branch to `main`** (this only needs to be done once):

  `git branch -M main`

- **Stage all changes for commit**:

  `git add .`

- **Commit your changes**:

  `git commit -m "Save local changes before pulling"`

- **Pull the latest changes from the remote repository**:

  `git pull origin main`

This will pull the latest changes from the remote `main` branch into your local repository.

#### 2.2. Stash Your Local Changes Before Pulling

If you want to temporarily save your local changes without committing them, you can stash them:

- **Link your local repository to the remote repository** (this only needs to be done once):

  `git remote add origin https://github.com/BlackFoxT/GradProject`

- **Set the default branch to `main`** (this only needs to be done once):

  `git branch -M main`

- **Stash your local changes**:

  `git stash`

- **Pull the latest changes from the remote repository**:

  `git pull origin main`

- **Restore your stashed changes** after pulling:

  `git stash pop`

This approach lets you save your work temporarily and pull the latest updates without losing any of your local changes.

#### 2.3. Discard Local Changes and Pull

If you don't need your local changes and want the latest version from the remote, you can discard all local changes:

- **Link your local repository to the remote repository** (this only needs to be done once)

  `git remote add origin https://github.com/BlackFoxT/GradProject`

- **Set the default branch to `main`** (this only needs to be done once):

  `git branch -M main`

- **Discard all local changes**:

  `git reset --hard`

- **Pull the latest changes from the remote repository**:

  `git pull origin main`

This approach will reset your local repository to the state of the remote `main` branch, discarding any uncommitted local changes.

---

### 3. Initial Push Operation

For new repositories, initialize Git and make your commit:

1. **Stage all files for commit**:

   `git add .`

2. **Commit your changes**:

   `git commit -m "your commit message"`

3. **Set the default branch to `main`** (this only needs to be done once):

   `git branch -M main`

4. **Link your local repository to the remote** (this only needs to be done once):

   `git remote add origin https://github.com/BlackFoxT/GradProject`

5. **Push your changes to the remote repository**:

   `git push -u origin main`

Once you've completed these steps, you'll be able to push changes directly to the `main` branch in future updates.

---

### Important Notes:

- `git remote add origin` should only be used once to link your local repository to the remote repository.
- `git pull origin main` pulls the latest changes from the remote `main` branch. If you're working with a different branch, replace `main` with the appropriate branch name.
- `git push -u origin main` pushes your local commits to the remote `main` branch. The `-u` flag sets the remote `main` branch as the default push target for future pushes.

---
