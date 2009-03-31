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
