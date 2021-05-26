# Ihufied
Ihufied is simply Ihu in a simplified version. Project Ihu is aimed at using facial recognition to mitigate examination impersonation. Ihufied contains only the web aspect of the project built with Flask framework, Bootstrap and other useful utilities.

## Getting Started
This simple guide is aimed to help you setup and run the program successfully in no time.

### Software Requirements
1. Install Git
2. Install Any programming editor(_Atom, Sublime, VSCode_)
3. Install the latest version of Python3

### Getting ready to run the program | Steps
1. Clone the the repository, `Ihufied`.
2. Create a virtual environment
3. Activate it and run ```pip install -r requirements.txt``` command on your terminal in the directory of the ihufied repository that is cloned on your PC or Mac. This will install all the necessary packages needed to run this program on your virtual environment.
4. In your terminal, run ```set FLASK_APP=ihufied.py```.
5. Run ```flask db upgrade```. To get your migration files in sync.

You can run the program now, by running ```python ihufied.py``` on the terminal. But things are not yet all set up, so the registration of student feature wouldn't work properly.

If you would be testing out the registration feature which uses the flask mail package to send a confirmation message. Then, there are still a couple of environment variables to set.

6. In the terminal, run ```MAIL_USERNAME=youraccount@gmail.com```, please replace `youraccount@gmail.com` with your personal gmail account.
7. Also, run `MAIL_PASSWORD=yourgmailpassword` similarly replace `yourgmailpassword` with the password to the corresponding gmail account

If you are bothered about security, try creating a secondary gmail account just for this. Also ensure to allow unsecured apps in the gmail settings of the account you provided above.

Also try changing the `MAIL_DEFAULT_SENDER` variable on line 12 of the `config.py` file to the your personal gmail account. If you have any issues you can try this quick fix, change the following settings in the config file.
1. `MAIL_USE_SSL` to `MAIL_USE_TLS`
2. Also, change the value in the `MAIL_PORT` variable from `465` to `587`.

Cheers!

