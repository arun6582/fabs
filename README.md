# fabs

## this project contains reusable fabric tasks for ubuntu and mac

You can install this by running

`pip install -e git+https://github.com/arun6582/fabs.git@master#egg=fabs`

If you want to just test how it works

`curl -sL https://raw.githubusercontent.com/arun6582/fabs/master/link_fabs.sh | bash -`

Run

`fab -l` to see list of fabric tasks

To install golang on a server

`fab packages.go-install -H sysadmin@139.59.23.11`

And you have go working in just under 15 secs.

I'm looking for contribution to increase number of fabs.

You can issue a pull request if you find some fab tasks which are reusable for others too.
