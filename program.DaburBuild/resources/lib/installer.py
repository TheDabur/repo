from __future__ import unicode_literals
from os import path
from urllib2 import urlopen
from zipfile import ZipFile
from xbmc import translatePath
from xml.dom import minidom
from distutils.version import StrictVersion
from re import findall
from time import sleep
from db import set_enabled, remove_addons
from shutil import rmtree
import xbmcvfs
import requests
import traceback
import xbmc
from xbmc import log as xbmclog

chunk_size = 1024 * 8


class Installer:
    repos = ["http://mirror.nl.leaseweb.net/xbmc/addons/krypton/",
             "https://raw.githubusercontent.com/kodil/kodil/master/",
             "https://raw.githubusercontent.com/cubicle-vdo/xbmc-israel/master/"]

    def __init__(self, addon_id, progress, lbl):
        self.addon_id = addon_id
        self.dp = progress
        self.repo_addons = {}
        self.versions = {}
        self.packages = set([])

        count = len(self.repos)
        for index, name in enumerate(self.repos, 1):
            self.dp.update(int(100.0 * index / count), lbl.format(index, count))
            self.get_repo_info(name)

    def clear_all(self, packages=[]):
        # disable all requested packages before removal
        if packages:
            set_enabled(packages, False)
            remove_addons(packages)
            # remove all requested packages excluding used packages
            dest = translatePath('special://home/addons')

            for p in packages:
                # execute StopScript(id) on scripts?
                self.log('removing old package {0} from {1}'.format(p, dest))
                rmtree(path.join(dest, p), True)

    def get_repo_info(self, repo):
        self.log('getting repo info {0}'.format(repo))

        try:
            r = urlopen(repo + "addons.xml")
            dom = minidom.parse(r)
            r.close()

            addons = dom.getElementsByTagName("addon")
            zip = repo
            if "xbmc-israel" in repo or "kodil" in repo:
                zip += "repo/"

            for addon in addons:
                try:
                    id = addon.getAttribute("id")
                    version = addon.getAttribute("version")
                    if (id not in self.versions or (
                                    version > 0 and StrictVersion(self.versions[id]) < StrictVersion(version))):
                        self.versions[id] = version
                        self.repo_addons[id] = '{0}{1}/{1}-{2}.zip'.format(zip, id, version)
                except Exception, e:
                    self.log("Error getting addon {0} info: {1}".format(id, str(e)), xbmc.LOGNOTICE)
        except:
            self.log("Error getting Repo XML {0}: {1}".format(repo, traceback.format_exc()), xbmc.LOGERROR)

    def download(self, src, dest, lbl='', level=0):
        self.log('{0}downloading {1}'.format('.' * (level), src))

        r = requests.get(src, stream=True, timeout=60)
        downloaded = True
        bytes_so_far = 0
        self.dp.update(0, lbl)

        try:
            total_size = int(r.headers['content-length'].strip())

            with open(dest, 'wb') as fp:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        bytes_so_far += len(chunk)
                        self.dp.update(int(100.0 * bytes_so_far / total_size))

                        fp.write(chunk)

                        if self.dp.iscanceled():
                            raise Exception("Canceled")
        except:
            downloaded = False
        finally:
            r.close()

        return downloaded

    def extract(self, src, dest, lbl='', level=0):
        self.log('{0}extracting to {1}'.format('.' * (level), dest))
        self.dp.update(0, lbl)
        try:
            with ZipFile(src, 'r') as zip:
                # with ZipFile(open(src, 'r')) as zip:
                files = zip.infolist()
                files_count = len(files)
                count = 0
                for file in files:
                    count += 1
                    self.dp.update(int(100.0 * count / files_count))
                    zip.extract(file, dest)

            return True
        except:
            self.log(traceback.format_exc(), xbmc.LOGERROR)

        return False

    def download_extract(self, src, dest, download_lbl='', extract_lbl='', id='', level=0):
        folder = translatePath(path.join('special://userdata/addon_data', self.addon_id)).encode('utf-8')
        tmpZip = path.join(folder, 'tmp.zip')
        xbmcvfs.mkdirs(folder)
        xbmcvfs.delete(tmpZip)

        retry = 0
        while not self.download(src, tmpZip, download_lbl, level=level) and retry < 5:
            retry += 1
            sleep(2)

        res = self.extract(tmpZip, dest, extract_lbl, level=level)
        xbmcvfs.delete(tmpZip)

        if res:
            if id:
                self.packages.add(id)
            return True

        self.log("download_extract error, id={0}, retries={1}".format(id, retry), xbmc.LOGERROR)
        return False

    def get(self, id, download_lbl='', extract_lbl='', level=0):
        url = self.repo_addons.get(id, '')
        dest = translatePath('special://home/addons')

        if url and self.download_extract(url, dest, download_lbl, extract_lbl, id=id, level=level):
            depends = path.join(dest, id, 'addon.xml')
            source = ''
            try:
                with open(depends, mode='r') as fp:
                    source = fp.read()
            except:
                self.log('file {0} for addon {1} doesn\'t exist!'.format(depends, id))
                return

            dependencies = findall(ur'import addon="(.+?)"', source)
            for dependency in dependencies:
                if not 'xbmc.' in dependency:
                    dependspath = path.join(dest, dependency)
                    if not path.exists(dependspath):
                        self.log('get dependency {0} for {1} (path {2} doesn\'t exist)'.format(dependency, id, dependspath))
                        self.get(dependency, download_lbl, extract_lbl, level=level + 1)
        else:
            self.log('error installing {0} ({1})'.format(id, url or "doesn't exist on repos"), xbmc.LOGERROR)

    def log(self, str, level=xbmc.LOGDEBUG, name='TheDabur'):
        """
            xbmc.LOGDEBUG   = 0
            xbmc.LOGINFO	= 1
            xbmc.LOGNOTICE  = 2
            xbmc.LOGWARNING = 3
            xbmc.LOGERROR   = 4
            xbmc.LOGSEVERE  = 5
            xbmc.LOGFATAL   = 6
            xbmc.LOGNONE	= 7
        """
        xbmclog('********** {0}: {1}'.format(name, str), level)
