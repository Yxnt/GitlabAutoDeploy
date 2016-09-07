#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, request
import json
from subprocess import call, Popen
from os import path, chdir

class conf():

    def __init__(self, conf):
        self.conf = conf

    def loadconf(self):
        with open(self.conf, 'rb') as f:
            jsoninfo = json.load(f)
            return jsoninfo

    def getrepositories(self):
        return self.loadconf()['repositories'][0]

    def getremoteurl(self):
        return self.getrepositories()['url']

    def getlocalpath(self):
        return self.getrepositories()['path']

    def getremote(self):
        return self.getrepositories()['remote']

    def getbranch(self):
        return self.getrepositories()['branch']


class gitlabapi():
    __c = conf('GitAutoDeploy.conf.json')
    localpath = __c.getlocalpath()
    repourl = __c.getremoteurl()
    remote = __c.getremote()
    branch = __c.getbranch()

    def __init__(self, jsoninfo):
        self.jsoninfo = jsoninfo

    def pull(self):
        jsoninfo = self.jsoninfo
        repo = jsoninfo['repository']
        sshurl = repo['url']
        httpurl = repo['git_http_url']

        if sshurl == self.repourl or httpurl == self.repourl :
            chdir(self.localpath)
            if path.exists(".git"):
                cmd = "git fetch {remote}".format(remote=self.remote) +\
                    '&& git reset --hard {remote}/{branch}'.format(
                            remote=self.remote,
                            branch=self.branch
                    ) + \
                    '&& git submodule init ' + \
                    '&& git submodule update' + \
                    '&& git update-index --refresh'
                res = Popen(cmd, shell=True)

                return res

            cmd = 'git clone --recursive {url} -b {branch} {path}'.format(
                url = self.repourl,
                branch = self.branch,
                path = self.localpath
            )
            res = call(cmd, shell=True)

            return res


app = Flask(__name__)
@app.route('/', methods=['POST'])
def index():
    response = json.loads(request.data)
    gitlabapi(response).pull()

    return ''



if __name__ == '__main__':
    app.run(
        host='10.1.13.126',
        debug=True,
    )

