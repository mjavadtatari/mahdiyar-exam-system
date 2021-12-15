**An Online Exam System Web App!**\
Powered by **Django 3** & **Python 3**

All requirements placed in `requirements.txt`\
To install **all-at-once**, first active **virtualenv**, the use this command in Terminal:
`pip install -r /path/to/requirements.txt`

To deploy the project on Linux Server Using: **Nginx**, **Gunicorn**, **Postgresql**\
Tutorial link form DigitalOcean : [How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04)

After making any changes to the codes, Run these two command in Linux Server Terminal:\
`sudo systemctl daemon-reload`\
`sudo systemctl restart gunicorn`

Install **Cerbot** on Ubuntu Server and enable **SSL** for **Nginx**:\
Tutorial link form DigitalOcean : [How To Secure Nginx with Let's Encrypt on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04)
