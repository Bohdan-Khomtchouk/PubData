from runwalker import ftpwalker

walker = ftpwalker('miRBase', 'mirbase.org', daemon=True)
walker.chek_state()
