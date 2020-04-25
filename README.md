# fabs

### This project contains reusable fabric tasks for ubuntu and mac

You can install this by running

`pip install -e git+https://github.com/arun6582/fabs.git@master#egg=fabs`

If you want to just test how it works

`curl -sL https://raw.githubusercontent.com/arun6582/fabs/master/link_fabs.sh | bash -`

Run

`fab -l` to see list of fabric tasks

To install golang on a server

`fab packages.go-install -H [user]@[host]`

And you have go working in just under 15 secs.

---

Say you want to start a ssh tunnel proxy service on a macbook pro which

All you need to do is run

`invoke patches.proxy 1 6666 [user]@[host] Wi-Fi --remote-port 22`

And fire up chrome and google search 'myip' and you will see ip is that of the server.

To turn that off run 

`invoke patches.proxy 0 6666 [user]@[host] Wi-Fi --remote-port 22`

---

#### I'm looking for contribution to increase number of fabs.

#### You can issue a pull request if you find some fab tasks which are reusable for others too.
