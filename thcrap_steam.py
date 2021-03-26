import os
import sys
import re
import glob
import configparser

def log(msg):
    logf.write('> %s\n'%(msg))

cfg = configparser.ConfigParser()
cfg.read(os.path.expanduser('~/.config/thcrap_steam.ini'))
data = cfg['script']
thcrap = os.path.expanduser(data.get('thcrap', '~/thcrap'))
patch = data.get('patch', 'en.js')
logfile = os.path.expanduser(data.get('log', '~/thcrap_steam.log'))

logf = open(logfile, "w+")

log('Read config file:')
log('    thcrap = "%s"'%(thcrap))
log('    patch = "%s"'%(patch))
log('    logfile = "%s"'%(logfile))
log('...')

inp = sys.argv[1]

log('Input = "%s"'%(inp))

thcrapexe = thcrap + '/bin/thcrap_loader.exe'
base = re.sub(r"'[^']+'[ ]*$", '', inp)
m = re.search(r'(th[0-9]+)\.exe', inp)

log('Prelim regex complete')

if m == None:
    log("Custom file...")
    # Determine the custom's pertaining game
    # by searching for the exe in the same dir
    f = re.search(r"'([^']+)'[ ]*$", inp).group(1)
    log('    f = "%s"'%(f))
    d = os.path.dirname(f)
    log('    d = "%s"'%(d))
    e = glob.glob(os.path.join(d, 'th*.exe'))[0]
    log('    e = "%s"'%(e))
    game = re.search(r'(th[0-9]+)\.exe$', e).group(1) + "_custom"
else:
    log('Launch game')
    game = m.group(1)

log("Game = " + game)

command = """
pushd '%s' > /dev/null
%s %s '%s' %s
popd > /dev/null
"""%(thcrap, base, thcrapexe, patch, game)

log('Executing: "%s"'%(command))

logf.close()

os.system(command)

