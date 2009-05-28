# TEMPORARY, NEVER EVER RELY ON IT.

import sjfs

def unlink(lid=-1, path=None):
    if lid != -1 and path is not None:
        return #Ambigious parameters
    fid = sjfs.get_fid(lid, path)
    if lid == -1:
        lid = sjfs.get_lid(path)
    if fid == 0 and not sjfs.file_exists(fid):
        raise sjfs.IOError(sjfs.SJFS_NOTFOUND, 'File not found.')
    sjfs.unlink(lid)

def list_files(path=None, full_data=False):
    if not path:
        path = '/'
    try:
        sjfs.set_current_chroot(sjfs.SJFS_BASEDIR)
        did = sjfs.get_did(path)
        if not did:
            return []
        values = sjfs.get_all_file_values_in_dir(did, False)
        links = values['dir']['links']
        files = values['files']
        final_links = []
        for link in links:
            updated_link = dict(link)
            updated_link.update({'size': values['files'][link['fid']]['size']})
            if full_data:
                updated_link.update({
                    'date'  : files[link['fid']]['categories']['common'].get('%d-creation_date' % link['fid'], 0),
                    'type'  : files[link['fid']]['categories']['common'].get('type', 'No type defined.'),
                    'md5'   : files[link['fid']]['categories']['common'].get('md5', 'No md5 defined'),
                })
            final_links.append(updated_link)
    finally:
        sjfs.set_current_chroot('/')
    return final_links

def get_free_space(path=sjfs.SJFS_BASEDIR):
    import os
    fsinfo = os.statvfs(path)
    free = fsinfo.f_bfree * fsinfo.f_frsize
    return free

def get_used_space(path=sjfs.SJFS_BASEDIR):
    import os
    fsinfo = os.statvfs(path)
    total = fsinfo.f_blocks * fsinfo.f_frsize
    free = fsinfo.f_bfree * fsinfo.f_frsize
    return total - free

def get_changelogs_versions(profile='rxtx'):
    import os
    all = []
    try:
        all = os.listdir('/usr/share/doc/sjchangelogs/%s/' % profile)
    except:
        return []

    # sort sources version in reverse order
    def cmp_version(x,y):
        x_list = map(int, x.split('.'))
        y_list = map(int, y.split('.'))
        return x_list < y_list and 1 or -1
    all.sort(cmp_version)

    return all

# Get raw changelog from /usr/share/doc/sjchangelogs/<profile>/<version>
# or html version of changelogs from /usr/share/doc/sjchangelogs/<profile>/<version>/default.html
# If page is specified, it will read /usr/share/doc/sjchangelogs/<profile>/<version>/<page>
def get_changelog(profile, version, page=None):
    import os.path
    out = ''
    path = '/usr/share/doc/sjchangelogs/%s/' % profile
    if os.path.exists(path+version+'/'):
        path += version + '/' + (page is not None and page or 'default.html')
    else:
        path += version
    try:
        log = open(path)
        for line in log:
            out += line
        log.close()
    except Exception, e:
        return None
    return out

def get_files_to_delete(max=10):
    from datetime import datetime
    import os.path
    files = []
    links = sjfs.get_links(sjfs.SJFS_FILE_CREATION_DATE)
    repo_len = len(sjfs.SJFS_BASEDIR) - 1
    for l in links:
        if len(files) >= max:
            break
        if l['path'].startswith(sjfs.SJFS_BASEDIR):
            keys = sjfs.get_keys_from_category(l['fid'], 'common')
            file = sjfs.get_file(l['fid'])
            basic_type = get_basic_type(l['lid'])
            preview = sjfs.get_key(l['fid'], 'snapshot', 'media') is not None or basic_type == 'image'
            files.append({
                'fid'       : l['fid'],
                'lid'       : l['lid'],
                'filename'  : l['filename'],
                'path'      : os.path.dirname(l['path'][repo_len:]),
                'md5'       : keys.get('md5', 'No md5 defined.'),
                'type'      : keys.get('type', 'No type defined.'),
                'date'      : datetime.fromtimestamp(float(keys.get('creation_date'))),
                'size'      : file.get('size',0),
                'preview'   : preview,
                'basic_type': basic_type,
                'deleted'   : False,
            })
    return files


# Make the preview for a file
# Store it in sjfs meta
def make_file_preview(fid, size=800):
    import tempfile, Image, os

    # Create tmp file
    _, tmp_path = tempfile.mkstemp(suffix='.preview',dir='/tmp')
    try:

        # Resize original image
        original = os.path.join(sjfs.SJFS_BASEDIR, sjfs.get_key(fid, 'current_filename'))
        preview = Image.open(original)
        preview.thumbnail((size, size))

        # Save to tmp
        preview.save(tmp_path, 'JPEG')

        # Store in meta
        tmp = open(tmp_path, 'r')
        meta = sjfs.open_file_meta(fid, 'snapshot', 'w', 'media')
        meta.write(tmp.read())

        # Close all fd and remove tmp
        meta.close()
        tmp.close()
        os.unlink(tmp_path)

    except:
        return False

    return True

# Get the preview picture for a file
def get_file_preview(fid):

    image = None
    try:
        # Try to make a preview
        if sjfs.get_key(fid, 'snapshot', 'media') is None:
            if not make_file_preview(fid, 100):
                return None

        # Read the preview
        fd = sjfs.open_file_meta(fid, "snapshot", "r", "media")
        image = fd.read()
        fd.close()
    except:
        return None
    return image

# Ping an host to check if it's alive
# Only one packet is sent with a timeout of 1 second
def ping(host):
    import popen2
    ping = popen2.Popen3('ping -c 1 -W 1 %s' % host)
    status = ping.wait()
    return (status == 0)

# Get the basic type for a link
# Used to display a correct icon
def get_basic_type(lid):
    import re

    types = {
        'image'     : ['^(PNG|JPEG|GIF) image data'],
        'media'     : [
            '^Microsoft ASF$', # wmv
            '^MPEG sequence', '^ISO Media, MPEG ', # mpg
            'Apple QuickTime movie', # mov
            '^Macromedia Flash Video$', # flv
            '^MPEG transport stream data$',
            '^(Material|General) Exchange Format', # mxf
            '^RIFF',
            '^DIF',
        ],
        'archive'   : [
            '^gzip compressed data,', # gz
            '^(POSIX )?tar archive', # tar
        ],
        'pdf'       : ['^PDF document,'],
        'xml'       : ['^XML 1.0 document text$'],
        'font'      : ['^TrueType font data$'],
        'exec'      : ['^Bourne(-Again)? shell script text executable$'],
        'text'      : ['^Microsoft Office Document$', '^ASCII text$'],
    }

    # Get the link type
    try:
        link = sjfs.get_link(lid)
        t = sjfs.get_key(link['fid'], 'type', 'common')
    except:
        return 'default'

    # Browse all checks
    for type_name, checks in types.items():
        for check in checks:
            if re.match(check, t):
                return type_name

    return 'default'
