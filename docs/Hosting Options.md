# Hosting Options

All of these require python 3.12 installed beforehand.

## IIS Local Server

Windows includes a service that lets you use you computer as a server. It needs to be enabled and configured, but will, when set up, allow you to host a website to those on the same wifi network as you.

### Setup

#### Internet Information Services

First, you need to enable IIS and related features. To do this, hit the windows key and search for `Turn Windows features on or off`. Close to the top of the list that this opens should be one labeled Internet Information Services. It's probably safe to just check beside it and then click okay, but this enables more features than needed.

Make sure the following are selected:

```txt
Internet Information Services/Web Management Tools/IIS Management Console
Internet Information Services/World Wide Web Services/Application Development Features/CGI
Internet Information Services/World Wide Web Services/Common HTTP Features/Default Document
Internet Information Services/World Wide Web Services/Common HTTP Features/Static Content
Internet Information Services/World Wide Web Services/Common HTTP Features/WebDAV Publishing
```

Some others may also be selected, but these are the ones that may or may not already be enabled.

##### Setting Connection to Program

TODO: see tutorial
    sources:
    https://medium.com/@dpralay07/deploy-a-python-flask-application-in-iis-server-and-run-on-machine-ip-address-ddb81df8edf3
    https://pypi.org/project/wfastcgi/
run wfastcgi-enable as admin from any command line
run as well, within the project folder:
    icacls . /grant "NT AUTHORITY\IUSR:(OI)(CI)(RX)"
    icacls . /grant "Builtin\IIS_IUSRS:(OI)(CI)(RX)"

add handler mappings to website
don't need to copy the fastcgi py file to root, just point to it at this stage
    see my setup for example

edit fastcgi application to add environment variable, see tutorial

currently, the flask runs on its own and the iis runs on its own, something is bad with the connection

#### Configuring You Network Settings

TODO: figure out exposing server to other computers on the network

#### Exposing Your Server to the Network

In order for others to access it, you need to configure you server. (The team should be able to configure the server for the client, by doing the following.)

1. Create a new site, with the root of the cloned git repository as its root.
    * Make sure default document is turned on, and that index.html is in the list.
2. Add a binding when creating the site.
    * HTTP, Port 70, and your new static IPv4 address.
    * As of right now, we are unsure as to how to get this working with an actual domain name, but it is likely a future feature wanted.

To open you server in your browser, click the link on the right under Browse Website.
