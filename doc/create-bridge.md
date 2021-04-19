# Create bridges

edit /etc/netplan/**.yaml

```yaml
network:
  ...
  bridges:
    br1: // bridge name
      addresses: [192.168.100.1/24]
      nameservers:
        addresses: [<dns server address>]
      dhcp4: false
      optional: true
    br2: // and more
```