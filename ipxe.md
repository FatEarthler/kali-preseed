# Prepare VPS host to serve the required files and protect them with a secret
## Host the installer under /var/www/ipxe
└─$ sudo mkdir -p /var/www/ipxe
└─$ sudo chmod 755 /var/www/ipxe
## Generate a long random token
└─$ TOKEN=$(openssl rand -hex 32)
└─$ echo $TOKEN
## Create an Nginx location that requires this token
└─$ sudo vim /etc/nginx/sites-available/ipxe.conf
```console
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    root /var/www/ipxe;

    # serve files normally, but protect them with token
    location / {
        # token must match as query parameter: ?token=XYZ
        if ($arg_token != "YOUR_RANDOM_TOKEN") {
            return 403;
        }

        # serve files
        try_files $uri =404;
    }
}
```
## Enable the site and reload Nginx
└─$ sudo ln -s /etc/nginx/sites-available/ipxe.conf /etc/nginx/sites-enabled/
└─$ sudo nginx -t
└─$ sudo systemctl reload nginx
## Test the protection

