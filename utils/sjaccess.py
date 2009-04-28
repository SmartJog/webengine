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

def get_changelogs_versions():
    import os
    all = []
    try:
        all = os.listdir('/etc/sjsmartchangelogs')
    except:
        return []

    # sort sources version in reverse order
    def cmp_version(x,y):
        x_list = map(int, x.split('.'))
        y_list = map(int, y.split('.'))
        return x_list < y_list and 1 or -1
    all.sort(cmp_version)

    return all

# Get raw changelog from /etc/sjsmartchangelogs
# or html version of changelogs from /etc/sjsmartchangelogs/<version>/changelog.html
# If page is specified, it will read /etc/sjsmartchangelogs/<version>/<page>
def get_changelog(version, page=None):
    import os.path
    out = ''
    path = '/etc/sjsmartchangelogs/'
    if os.path.exists(path+version+'/'):
        path += version + '/' + (page is not None and page or 'changelog.html')
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
    files = []
    links = sjfs.get_links(sjfs.SJFS_FILE_CREATION_DATE)
    for l in links:
        if len(files) >= max:
            break
        if l['path'].startswith(sjfs.SJFS_BASEDIR):
            keys = sjfs.get_keys_from_category(l['fid'], 'common')
            files.append({
                'fid'       : l['fid'],
                'lid'       : l['lid'],
                'filename'  : l['filename'],
                'path'      : l['path'],
                'md5'       : keys.get('md5', 'No md5 defined.'),
                'type'      : keys.get('type', 'No type defined.'),
                'date'      : datetime.fromtimestamp(float(keys.get('creation_date'))),
                'size'      : 0,
                'preview'   : sjfs.get_key(l['fid'], 'snapshot', 'media') is not None,
            })
    return files

def get_file_preview(fid):
    image = None
    try:
        fd = sjfs.open_file_meta(fid, "snapshot", "r", "media")
        image = fd.read()
        fd.close()
    except:
        return None
    return image
