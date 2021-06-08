## coder-cloud-redirect-server

A very simple server that simplifies connections to your server started with code-server link. Currently only works by searching logs for the systemd service.

Usage:
```sh
$ ./server.py [port]
```

## Troubleshooting

If you are being redirected to this screen, that means the redirect service is working, but is unable to read the code-server status.

```sh
# Check if code-server is running
systemctl status code-server@coder

# Check if journalctl is giving us logs
journalctl -u code-server@coder

# If journalctl isn't giving logs:
systemd restart systemd-journald 
# or
sed -i.bak 's/#Storage=auto/Storage=persistent/' /etc/systemd/journald.conf
mkdir -p /var/log/journal
systemctl force-reload systemd-journald
systemctl restart systemd-journald
# then, if needed:
sudo reboot
```
