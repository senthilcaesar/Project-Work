# To create local repository

mkdir newproject
cd newproject

# Next we need to initialize the repository

git init

# Next we need to add a file to the project

touch readme.txt

# Now you will have an empty file in your repository

git status

# Even though git is aware of the file, it has not been added to the project

git add readme.txt
git status

# Your First commit, commit is a record of the file you have changed within the project
# Before we do this, we have to inform Git who we are

git config --global user.email senthilcaesar@yahoo.co.in
git config --global user.name senthilcaesar

# New we can create the commit

git commit -m "test message"

# Create a branch and push it to GitHub

git checkout -b gamemodules
git branch

# Next we need to create a repository on GitHub, Click the new repository button from
# your main page and click create repository
# After creating the repository you will be presented with a URL to use for pushing our new created local repository

git remote add origin https://github.com/SenthilCaesar/testapp
git push -u origin game

# Pulling the project
# Say your collaborators make changes to the code on the GitHub project and have merged those changes

git pull origin game

# clone branch
git clone -b remove-ext-dep https://github.com/pnlbwh/CNN-Diffusion-MRIBrain-Segmentation



# Example1
	# Pull the latest changes from branch
	git pull origin remove-ext-dep

	# Create new branch
	git checkout -b clean-imports

	# make the changes and commit it
	git push -u origin clean-imports
	
# When the user wants to intall your module from pip python or conda packages
# you will have to release your developed code in the github release tab
