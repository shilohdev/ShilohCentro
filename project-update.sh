#!/bin/bash
cd
cd
rm -rf /usr/local/project/ShilohCentro
rm -rf /usr/local/project
mkdir /usr/local/project
cd /usr/local/project
git clone https://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@github.com/shilohdev/ShilohCentro.git
cd
cd /usr/local/shilohcentro
sudo rm -rf auth_access
sudo rm -rf auth_users
sudo rm -rf initialize
sudo rm -rf shiloh
sudo rm -rf static
sudo rm -rf accounts
sudo rm -rf auth_finances
sudo rm -rf functions
sudo rm -rf templates
sudo mv /usr/local/project/ShilohCentro/auth_access /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/auth_users /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/initialize /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/shiloh /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/accounts /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/auth_finances /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/auth_permissions /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/functions /usr/local/shilohcentro
sudo mv /usr/local/project/ShilohCentro/templates /usr/local/shilohcentro
cd
cd /usr/local/shilohcentro
source shilohenv/bin/activate
python manage.py collectstatic --noinput
deactivate
sudo systemctl restart gunicorn
cd
cd
cd
rm -rf /usr/local/project/ShilohCentro
rm -rf /usr/local/project
cd
exit

