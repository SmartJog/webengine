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

def list_files(path=None):
    if not path:
        path = sjfs.SJFS_BASEDIR
    try:
        sjfs.set_current_chroot(path)
        links = sjfs.get_links()
    finally:
        sjfs.set_current_chroot('/')
    return links

def get_free_space(path=sjfs.SJFS_BASEDIR):
    import os
    fsinfo = os.statvfs(path)
    free = fsinfo.f_bfree * fsinfo.f_frsize
    freeGB = (float(free) / 1024.0 / 1024.0 / 1024.0)
    freeMB = (float(free) / 1024.0 / 1024.0)
    if freeGB > 1:
        return "%.2fG" % freeGB
    return "%.2fM" % freeMB

def get_used_space(path=sjfs.SJFS_BASEDIR):
    import os
    fsinfo = os.statvfs(path)
    total = fsinfo.f_blocks * fsinfo.f_frsize
    free = fsinfo.f_bfree * fsinfo.f_frsize
    used = total - free
    usedGB = (float(used) / 1024.0 / 1024.0 / 1024.0)
    usedMB = (float(used) / 1024.0 / 1024.0)
    if usedGB > 1:
        return "%.2fG" % usedGB
    return "%.2fM" % usedMB
