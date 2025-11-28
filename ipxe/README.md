# Prepare Debian VPS host to serve the required files and protect them
The VPS host will use a self signed TLS certificate which will be pinned by the ipxe client. Furthermore, requests to the host will use a timestamp, machine code and HMAC over those two attributes, based on a shared secret (master.key). Request without valid HMAC, (proof of posession of master.key) get rejected. The timestamp will also be validated and requests which are too old will get rejected.

## Setup the server with https and HMAC using nginx and lua
### Install nginx and lua http mod (required for HMAC)
└─$ sudo apt install nginx libnginx-mod-http-lua
### Generate a self signed. X.509 certificate:
└─$ vim ~/cert.conf
```console
[req]
default_bits       = 4096
prompt             = no
default_md         = sha256
req_extensions     = req_ext
distinguished_name = dn

[dn]
CN = 83.228.213.33

[req_ext]
subjectAltName = @alt_names

[alt_names]
IP.1 = 83.228.213.33
```
└─$ sudo openssl req \
  -newkey rsa:4096 -nodes \
  -x509 -sha256 \
  -days 3650 \
  -keyout /etc/ssl/private/pxe-server.key \
  -out /etc/ssl/certs/pxe-server.crt \
  -config ~/cert.conf
  -extensions req_ext

└─$ sudo chmod 600 /etc/ssl/private/pxe-server.key

└─$ sudo chmod 644 /etc/ssl/certs/pxe-server.crt
### Host the ipxe server under /var/www/ipxe
└─$ sudo mkdir -p /var/www/ipxe

└─$ sudo chmod 755 /var/www/ipxe
### Create the master.key file
└─$ echo $(openssl rand -hex 32) | sudo tee -a /etc/nginx/master.key
### Create an nginx location that uses the just created certificates
└─$ sudo vim /etc/nginx/sites-available/ipxe.conf
```console
server {
    listen 443 ssl;
    server_name _;

    ssl_certificate     /etc/ssl/certs/pxe-server.crt;
    ssl_certificate_key /etc/ssl/private/pxe-server.key;

    # Only modern TLS
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    # Strong ciphers
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        access_by_lua_block {
            local bit = require "bit"  -- bitwise operations
            local ngx_sha256_bin = ngx.sha256_bin
            local ngx_encode_base64 = ngx.encode_base64

            -- Load secret (you can also read from a file for security)
            local f = io.open("/etc/nginx/master.key", "r")
            local secret = f:read("*all"):gsub("%s+", "")
            f:close()

            local headers = ngx.req.get_headers()
            local timestamp = headers["X-Timestamp"]
            local machine_id = headers["X-Machine-ID"]
            local signature = headers["X-Signature"]

            -- Reject if headers missing
            if not timestamp or not machine_id or not signature then
                return ngx.exit(ngx.HTTP_FORBIDDEN)
            end

            -- Reject if timestamp is too old (5 minutes)
            local ts_num = tonumber(timestamp)
            if not ts_num or math.abs(ngx.time() - ts_num) > 300 then
                return ngx.exit(ngx.HTTP_FORBIDDEN)
            end

            -- Pure Lua HMAC-SHA256
            local function hmac_sha256(key, msg)
                local block_size = 64
                if #key > block_size then
                    key = ngx_sha256_bin(key)
                end
                if #key < block_size then
                    key = key .. string.rep("\0", block_size - #key)
                end

                local o_key_pad = ""
                local i_key_pad = ""
                for i = 1, #key do
                    local b = string.byte(key, i)
                    o_key_pad = o_key_pad .. string.char(bit.bxor(b, 0x5c))
                    i_key_pad = i_key_pad .. string.char(bit.bxor(b, 0x36))
                end

                local inner = ngx_sha256_bin(i_key_pad .. msg)
                return ngx_encode_base64(ngx_sha256_bin(o_key_pad .. inner))
            end

            local expected_signature = hmac_sha256(secret, timestamp .. machine_id)

            if expected_signature ~= signature then
                return ngx.exit(ngx.HTTP_FORBIDDEN)
            end
        }

        root /var/www/ipxe;
    }
}
```
### Enable the site and reload Nginx
└─$ sudo ln -s /etc/nginx/sites-available/ipxe.conf /etc/nginx/sites-enabled/

└─$ sudo nginx -t

└─$ sudo systemctl reload nginx
